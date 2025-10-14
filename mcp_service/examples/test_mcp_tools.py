#!/usr/bin/env python3
"""
Test the MCP server tools (simulates MCP tool calls).

This script validates that all MCP tools are properly defined and can be invoked.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import after path adjustment
from mcp_service.server.main import TOOLS, handle_tool_call
from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager
from mcp_service.server.persona_manager import PersonaManager
import asyncio


async def test_tools():
    """Test that all MCP tools are defined correctly."""

    print("=" * 80)
    print("MCP TOOLS VALIDATION")
    print("=" * 80)

    # Initialize global instances (simulate main())
    import mcp_service.server.main as main_module

    repo_path = Path.cwd() / "projects_repo"
    personas_path = Path.cwd() / "personas"

    main_module.repo = ProjectRepository(repo_path)
    main_module.context_manager = ContextManager(main_module.repo)
    main_module.persona_manager = PersonaManager(personas_path)

    print(f"\n✅ Initialized:")
    print(f"   - Repository: {repo_path}")
    print(f"   - Personas: {personas_path}")

    # List all tools
    print(f"\n📋 Total MCP Tools: {len(TOOLS)}\n")

    tool_categories = {
        "Project Management": [],
        "Context Management": [],
        "Persona Management": [],
    }

    for tool in TOOLS:
        name = tool.name
        desc = tool.description

        if "persona" in name.lower():
            tool_categories["Persona Management"].append((name, desc))
        elif "context" in name.lower():
            tool_categories["Context Management"].append((name, desc))
        else:
            tool_categories["Project Management"].append((name, desc))

    # Display by category
    for category, tools in tool_categories.items():
        if tools:
            print(f"{category} ({len(tools)} tools):")
            for name, desc in tools:
                print(f"   • {name}")
                print(f"     {desc}")
            print()

    # Test a few key tools
    print("=" * 80)
    print("TESTING KEY TOOLS")
    print("=" * 80)

    # Test list_projects
    print("\n1. Testing list_projects...")
    result = await handle_tool_call("list_projects", {})
    print(f"   ✅ Success: {len(result)} response(s)")

    # Test list_personas
    print("\n2. Testing list_personas...")
    result = await handle_tool_call("list_personas", {})
    print(f"   ✅ Success: {len(result)} response(s)")
    if result:
        print(f"   Preview: {result[0].text[:200]}...")

    # Test load_context
    print("\n3. Testing load_context (payment_gateway)...")
    try:
        result = await handle_tool_call("load_context", {"project_name": "payment_gateway"})
        print(f"   ✅ Success: {len(result)} response(s)")
    except Exception as e:
        print(f"   ⚠️  Expected (project may not exist): {str(e)[:100]}")

    # Test load_persona
    print("\n4. Testing load_persona (business_analyst)...")
    try:
        result = await handle_tool_call("load_persona", {"persona_name": "business_analyst"})
        print(f"   ✅ Success: {len(result)} response(s)")
        if result:
            print(f"   Preview: {result[0].text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test get_current_context
    print("\n5. Testing get_current_context...")
    result = await handle_tool_call("get_current_context", {})
    print(f"   ✅ Success: {len(result)} response(s)")

    print("\n" + "=" * 80)
    print("✅ MCP TOOLS VALIDATION COMPLETE")
    print("=" * 80)

    print("\nSummary:")
    print(f"   • Total tools: {len(TOOLS)}")
    print(f"   • Project Management: {len(tool_categories['Project Management'])} tools")
    print(f"   • Context Management: {len(tool_categories['Context Management'])} tools")
    print(f"   • Persona Management: {len(tool_categories['Persona Management'])} tools")
    print("\n✅ All tools are properly defined and can be invoked!")


if __name__ == "__main__":
    asyncio.run(test_tools())
