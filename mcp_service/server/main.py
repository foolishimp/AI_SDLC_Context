#!/usr/bin/env python3
"""
MCP Server for ai_sdlc_method.

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
from .context_tools import ContextManager
from .persona_manager import PersonaManager


# Global instances
repo: Optional[ProjectRepository] = None
context_manager: Optional[ContextManager] = None
persona_manager: Optional[PersonaManager] = None


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
    # Context Management Tools
    Tool(
        name="load_context",
        description="Load a project context for Claude to work with",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Project name to load context for"
                }
            },
            "required": ["project_name"]
        }
    ),
    Tool(
        name="switch_context",
        description="Switch from current context to a different project context",
        inputSchema={
            "type": "object",
            "properties": {
                "new_project": {
                    "type": "string",
                    "description": "Project name to switch to"
                }
            },
            "required": ["new_project"]
        }
    ),
    Tool(
        name="query_context",
        description="Query the current context for specific information",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What to query (e.g., 'testing requirements', 'security policies')"
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="get_current_context",
        description="Get information about the currently loaded context",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="get_full_context_state",
        description="Get comprehensive view of entire context state including layers, merges, and materialized config",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    # Persona Management Tools
    Tool(
        name="list_personas",
        description="List all available personas (roles like business_analyst, qa_engineer, etc.)",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="load_persona",
        description="Load a persona to customize how Claude views the project",
        inputSchema={
            "type": "object",
            "properties": {
                "persona_name": {
                    "type": "string",
                    "description": "Persona name (e.g., 'business_analyst', 'software_engineer', 'qa_engineer')"
                }
            },
            "required": ["persona_name"]
        }
    ),
    Tool(
        name="apply_persona_to_context",
        description="Apply a persona to the current project context",
        inputSchema={
            "type": "object",
            "properties": {
                "persona_name": {
                    "type": "string",
                    "description": "Persona name to apply"
                },
                "project_name": {
                    "type": "string",
                    "description": "Project name (uses current context if not specified)"
                }
            },
            "required": ["persona_name"]
        }
    ),
    Tool(
        name="switch_persona",
        description="Switch from one persona to another and see what changed",
        inputSchema={
            "type": "object",
            "properties": {
                "from_persona": {
                    "type": "string",
                    "description": "Current persona name (optional)"
                },
                "to_persona": {
                    "type": "string",
                    "description": "Target persona name"
                }
            },
            "required": ["to_persona"]
        }
    ),
    Tool(
        name="get_persona_checklist",
        description="Get the review checklist for a specific persona",
        inputSchema={
            "type": "object",
            "properties": {
                "persona_name": {
                    "type": "string",
                    "description": "Persona name (uses current persona if not specified)"
                }
            }
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
    global repo, context_manager, persona_manager

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

        # Context Management Tools
        elif name == "load_context":
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            context = context_manager.load_context(arguments["project_name"])
            formatted = context_manager.format_context_for_llm(context)

            return [TextContent(
                type="text",
                text=formatted
            )]

        elif name == "switch_context":
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            result = context_manager.switch_context(arguments["new_project"])

            response = f"Switched context to: {result['new_project']}\n\n"
            if result.get('requirements_changed'):
                response += "Requirements that changed:\n"
                for change in result['requirements_changed']:
                    response += f"  • {change}\n"

            return [TextContent(
                type="text",
                text=response
            )]

        elif name == "query_context":
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            result = context_manager.query_context(arguments["query"])

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_current_context":
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            if context_manager.current_context is None:
                return [TextContent(
                    type="text",
                    text="No context currently loaded"
                )]

            context_name = context_manager.current_context.get('metadata', {}).get('name', 'Unknown')
            formatted = context_manager.format_context_for_llm(context_manager.current_context)

            return [TextContent(
                type="text",
                text=f"Current Context: {context_name}\n\n{formatted}"
            )]

        elif name == "get_full_context_state":
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            state = context_manager.get_full_context_state()

            # Import the formatter
            from .context_tools import format_full_context_state
            formatted = format_full_context_state(state)

            return [TextContent(
                type="text",
                text=formatted
            )]

        # Persona Management Tools
        elif name == "list_personas":
            if persona_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Persona manager not initialized"
                )]

            personas = persona_manager.list_personas()

            response = f"Available Personas ({len(personas)}):\n\n"
            for persona in personas:
                response += f"👤 {persona['name']} ({persona['role']})\n"
                response += f"   Focus: {', '.join(persona['focus_areas'][:3])}\n\n"

            return [TextContent(
                type="text",
                text=response
            )]

        elif name == "load_persona":
            if persona_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Persona manager not initialized"
                )]

            persona = persona_manager.load_persona(arguments["persona_name"])

            response = f"Loaded Persona: {persona['persona']['name']}\n\n"
            response += "Focus Areas:\n"
            for focus in persona['persona']['focus_areas']:
                response += f"  • {focus}\n"

            return [TextContent(
                type="text",
                text=response
            )]

        elif name == "apply_persona_to_context":
            if persona_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Persona manager not initialized"
                )]
            if context_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Context manager not initialized"
                )]

            # Load persona
            persona = persona_manager.load_persona(arguments["persona_name"])

            # Get project context
            if "project_name" in arguments:
                project_context = context_manager.load_context(arguments["project_name"])
            elif context_manager.current_context:
                project_context = context_manager.current_context
            else:
                return [TextContent(
                    type="text",
                    text="Error: No context loaded. Specify project_name or load a context first."
                )]

            # Apply persona to context
            persona_context = persona_manager.apply_persona_to_context(project_context, persona)

            # Format for display
            formatted = persona_manager.format_context_for_persona(persona_context, persona)

            return [TextContent(
                type="text",
                text=formatted
            )]

        elif name == "switch_persona":
            if persona_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Persona manager not initialized"
                )]

            result = persona_manager.switch_persona(
                arguments.get("from_persona"),
                arguments["to_persona"]
            )

            response = f"Switched to: {result['to']}\n\n"
            if result.get('focus_changed'):
                if result['focus_changed'].get('added_focus'):
                    response += "Added Focus Areas:\n"
                    for focus in result['focus_changed']['added_focus']:
                        response += f"  ✚ {focus}\n"
                if result['focus_changed'].get('removed_focus'):
                    response += "\nRemoved Focus Areas:\n"
                    for focus in result['focus_changed']['removed_focus']:
                        response += f"  ✖ {focus}\n"

            return [TextContent(
                type="text",
                text=response
            )]

        elif name == "get_persona_checklist":
            if persona_manager is None:
                return [TextContent(
                    type="text",
                    text="Error: Persona manager not initialized"
                )]

            checklist = persona_manager.get_persona_review_checklist(
                arguments.get("persona_name")
            )

            if not checklist:
                return [TextContent(
                    type="text",
                    text="No checklist available for this persona"
                )]

            response = "Review Checklist:\n\n"
            for item in checklist:
                response += f"□ {item}\n"

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


async def main(repo_path: Optional[str] = None, personas_path: Optional[str] = None):
    """
    Run the MCP server.

    Args:
        repo_path: Path to project repository (defaults to ./projects_repo)
        personas_path: Path to personas directory (defaults to ./personas)
    """
    global repo, context_manager, persona_manager

    # Initialize repository
    if repo_path is None:
        repo_path = Path.cwd() / "projects_repo"
    else:
        repo_path = Path(repo_path)

    repo = ProjectRepository(repo_path)

    # Initialize context manager
    context_manager = ContextManager(repo)

    # Initialize persona manager
    if personas_path is None:
        personas_path = Path.cwd() / "personas"
    else:
        personas_path = Path(personas_path)

    persona_manager = PersonaManager(personas_path)

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

    parser = argparse.ArgumentParser(description="ai_sdlc_method MCP Server")
    parser.add_argument(
        "--repo-path",
        help="Path to project repository (default: ./projects_repo)"
    )
    parser.add_argument(
        "--personas-path",
        help="Path to personas directory (default: ./personas)"
    )
    args = parser.parse_args()

    asyncio.run(main(args.repo_path, args.personas_path))
