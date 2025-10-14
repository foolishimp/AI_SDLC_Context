#!/usr/bin/env python3
"""
MCP Server for AI_SDLC_config.

Provides Model Context Protocol interface for managing configuration projects.
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

from ..storage.project_repository import ProjectRepository


# Global repository instance
repo: Optional[ProjectRepository] = None


# Tool definitions
TOOLS = [
    Tool(
        name="create_project",
        description="Create a new configuration project",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Project name (must be unique)"
                },
                "type": {
                    "type": "string",
                    "enum": ["base", "methodology", "custom"],
                    "description": "Project type"
                },
                "base_projects": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of base project names to inherit from"
                },
                "config": {
                    "type": "object",
                    "description": "Initial configuration (optional)"
                },
                "description": {
                    "type": "string",
                    "description": "Project description (optional)"
                }
            },
            "required": ["name", "type", "base_projects"]
        }
    ),
    Tool(
        name="get_project",
        description="Get project metadata and information",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Project name"
                }
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="list_projects",
        description="List all projects in the repository",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="update_project",
        description="Update project configuration values",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Project name"
                },
                "updates": {
                    "type": "object",
                    "description": "Dict of dot-path to value updates (e.g., {'methodology.testing.min_coverage': 95})"
                }
            },
            "required": ["name", "updates"]
        }
    ),
    Tool(
        name="delete_project",
        description="Delete a project from the repository",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Project name"
                }
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="add_node",
        description="Add a configuration node to a project",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project name"
                },
                "path": {
                    "type": "string",
                    "description": "Dot-delimited path (e.g., 'security.fraud_detection')"
                },
                "value": {
                    "description": "Value to set at the path"
                }
            },
            "required": ["project", "path", "value"]
        }
    ),
    Tool(
        name="remove_node",
        description="Remove a configuration node from a project",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project name"
                },
                "path": {
                    "type": "string",
                    "description": "Dot-delimited path to remove"
                }
            },
            "required": ["project", "path"]
        }
    ),
    Tool(
        name="add_document",
        description="Add a documentation file to a project",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project name"
                },
                "path": {
                    "type": "string",
                    "description": "Relative path within docs/ (e.g., 'policies/security.md')"
                },
                "content": {
                    "type": "string",
                    "description": "Document content"
                }
            },
            "required": ["project", "path", "content"]
        }
    ),
    Tool(
        name="merge_projects",
        description="Merge multiple projects into a new merged project",
        inputSchema={
            "type": "object",
            "properties": {
                "source_projects": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of project names to merge (in priority order)"
                },
                "target_project": {
                    "type": "string",
                    "description": "Name for the new merged project"
                },
                "runtime_overrides": {
                    "type": "object",
                    "description": "Additional runtime overrides to apply (optional)"
                },
                "description": {
                    "type": "string",
                    "description": "Description for merged project (optional)"
                }
            },
            "required": ["source_projects", "target_project"]
        }
    ),
    Tool(
        name="inspect_project",
        description="Query and inspect a project using natural language (LLM-powered)",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project name"
                },
                "query": {
                    "type": "string",
                    "description": "Natural language query about the project"
                }
            },
            "required": ["project", "query"]
        }
    ),
    Tool(
        name="compare_projects",
        description="Compare two projects and highlight differences (LLM-powered)",
        inputSchema={
            "type": "object",
            "properties": {
                "project1": {
                    "type": "string",
                    "description": "First project name"
                },
                "project2": {
                    "type": "string",
                    "description": "Second project name"
                },
                "query": {
                    "type": "string",
                    "description": "What to compare (e.g., 'testing requirements')"
                }
            },
            "required": ["project1", "project2"]
        }
    ),
]


async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle MCP tool calls.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of TextContent responses
    """
    global repo

    try:
        if name == "create_project":
            metadata = repo.create_project(
                name=arguments["name"],
                project_type=arguments["type"],
                base_projects=arguments["base_projects"],
                config=arguments.get("config"),
                description=arguments.get("description")
            )
            return [TextContent(
                type="text",
                text=json.dumps(metadata.__dict__, indent=2)
            )]

        elif name == "get_project":
            metadata = repo.get_project(arguments["name"])
            if metadata is None:
                return [TextContent(
                    type="text",
                    text=f"Project '{arguments['name']}' not found"
                )]
            return [TextContent(
                type="text",
                text=json.dumps(metadata.__dict__, indent=2)
            )]

        elif name == "list_projects":
            projects = repo.list_projects()
            result = [
                {
                    "name": p.name,
                    "type": p.project_type,
                    "base_projects": p.base_projects,
                    "description": p.description
                }
                for p in projects
            ]
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "update_project":
            metadata = repo.update_project(
                name=arguments["name"],
                updates=arguments["updates"]
            )
            return [TextContent(
                type="text",
                text=json.dumps(metadata.__dict__, indent=2)
            )]

        elif name == "delete_project":
            repo.delete_project(arguments["name"])
            return [TextContent(
                type="text",
                text=f"Project '{arguments['name']}' deleted successfully"
            )]

        elif name == "add_node":
            updates = {arguments["path"]: arguments["value"]}
            metadata = repo.update_project(
                name=arguments["project"],
                updates=updates
            )
            return [TextContent(
                type="text",
                text=f"Added node '{arguments['path']}' to project '{arguments['project']}'"
            )]

        elif name == "remove_node":
            # Remove by setting to None (triggers deletion in merge)
            updates = {arguments["path"]: None}
            metadata = repo.update_project(
                name=arguments["project"],
                updates=updates
            )
            return [TextContent(
                type="text",
                text=f"Removed node '{arguments['path']}' from project '{arguments['project']}'"
            )]

        elif name == "add_document":
            doc_path = repo.add_document(
                project_name=arguments["project"],
                doc_path=arguments["path"],
                content=arguments["content"]
            )
            return [TextContent(
                type="text",
                text=f"Document added at: {doc_path}"
            )]

        elif name == "merge_projects":
            metadata = repo.merge_projects(
                source_projects=arguments["source_projects"],
                target_name=arguments["target_project"],
                runtime_overrides=arguments.get("runtime_overrides"),
                description=arguments.get("description")
            )
            return [TextContent(
                type="text",
                text=json.dumps(metadata.__dict__, indent=2)
            )]

        elif name == "inspect_project":
            # Get project config
            config_manager = repo.get_project_config(arguments["project"])
            if config_manager is None:
                return [TextContent(
                    type="text",
                    text=f"Project '{arguments['project']}' not found"
                )]

            # Convert hierarchy to JSON for LLM context
            import yaml
            from ai_sdlc_config.models.hierarchy_node import URIReference

            def hierarchy_to_dict(node) -> Dict[str, Any]:
                if node.value is not None and not node.children:
                    if isinstance(node.value, URIReference):
                        # Try to resolve content
                        try:
                            content = config_manager.get_content(node.path)
                            return {"uri": node.value.uri, "content": content[:500]}  # Preview
                        except:
                            return {"uri": node.value.uri}
                    else:
                        return node.value

                result = {}
                for key, child in node.children.items():
                    result[key] = hierarchy_to_dict(child)
                return result

            config_data = hierarchy_to_dict(config_manager.merged_hierarchy)

            # Format response for LLM
            response = f"Project: {arguments['project']}\n\n"
            response += f"Query: {arguments['query']}\n\n"
            response += "Configuration:\n"
            response += yaml.dump(config_data, default_flow_style=False)

            return [TextContent(
                type="text",
                text=response
            )]

        elif name == "compare_projects":
            # Get both project configs
            config1 = repo.get_project_config(arguments["project1"])
            config2 = repo.get_project_config(arguments["project2"])

            if config1 is None:
                return [TextContent(
                    type="text",
                    text=f"Project '{arguments['project1']}' not found"
                )]

            if config2 is None:
                return [TextContent(
                    type="text",
                    text=f"Project '{arguments['project2']}' not found"
                )]

            # Simple comparison (could be enhanced with LLM)
            import yaml
            from ai_sdlc_config.models.hierarchy_node import URIReference

            def hierarchy_to_dict(node) -> Dict[str, Any]:
                if node.value is not None and not node.children:
                    if isinstance(node.value, URIReference):
                        return {"uri": node.value.uri}
                    else:
                        return node.value

                result = {}
                for key, child in node.children.items():
                    result[key] = hierarchy_to_dict(child)
                return result

            data1 = hierarchy_to_dict(config1.merged_hierarchy)
            data2 = hierarchy_to_dict(config2.merged_hierarchy)

            response = f"Comparison: {arguments['project1']} vs {arguments['project2']}\n\n"
            if "query" in arguments:
                response += f"Focus: {arguments['query']}\n\n"

            response += f"{arguments['project1']} Configuration:\n"
            response += yaml.dump(data1, default_flow_style=False)
            response += f"\n{arguments['project2']} Configuration:\n"
            response += yaml.dump(data2, default_flow_style=False)

            return [TextContent(
                type="text",
                text=response
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main(repo_path: Optional[str] = None):
    """
    Run the MCP server.

    Args:
        repo_path: Path to project repository (defaults to ./projects_repo)
    """
    global repo

    # Initialize repository
    if repo_path is None:
        repo_path = Path.cwd() / "projects_repo"
    else:
        repo_path = Path(repo_path)

    repo = ProjectRepository(repo_path)

    # Create server
    server = Server("ai-sdlc-config")

    # Register tools
    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]):
        return await handle_tool_call(name, arguments)

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI_SDLC_config MCP Server")
    parser.add_argument(
        "--repo-path",
        help="Path to project repository (default: ./projects_repo)"
    )
    args = parser.parse_args()

    asyncio.run(main(args.repo_path))
