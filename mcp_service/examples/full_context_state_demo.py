#!/usr/bin/env python3
"""
Demo: Full Context State Display

This demonstrates the complete context state visualization showing:
1. All configuration layers
2. Merge order
3. Active persona
4. Materialized (merged) configuration
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager, format_full_context_state
from mcp_service.server.persona_manager import PersonaManager


def main():
    """Run full context state demo."""
    print("=" * 80)
    print("FULL CONTEXT STATE DEMO")
    print("=" * 80)
    print()

    # Initialize components
    repo_path = Path(__file__).parent.parent / "projects_repo"
    repo = ProjectRepository(root_path=repo_path)
    context_manager = ContextManager(repository=repo)
    persona_manager = PersonaManager(personas_dir=Path(__file__).parent.parent.parent / "personas")

    # Demo 1: Context without persona
    print("📋 Demo 1: Loading context WITHOUT persona")
    print("-" * 80)
    context = context_manager.load_context("payment_gateway")
    state = context_manager.get_full_context_state()
    formatted = format_full_context_state(state)
    print(formatted)
    print()

    # Demo 2: Context WITH persona
    print()
    print("📋 Demo 2: Loading context WITH security engineer persona")
    print("-" * 80)

    # Load persona
    persona = persona_manager.load_persona("security_engineer")

    # Apply persona to context
    context_with_persona = persona_manager.apply_persona_to_context(context, persona)

    # Update context manager with persona-enhanced context
    context_manager.current_context = context_with_persona

    # Get full state
    state = context_manager.get_full_context_state()
    formatted = format_full_context_state(state)
    print(formatted)
    print()

    # Demo 3: Explain the layers
    print()
    print("📋 Demo 3: Understanding the Layer Stack")
    print("-" * 80)
    print("""
The context state shows the complete configuration merge process:

LAYER STACK (lowest → highest priority):
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Corporate Base (01_corporate_base.yml)                 │
│   - Company-wide standards                                       │
│   - Default policies                                             │
│   - Base quality requirements                                    │
└─────────────────────────────────────────────────────────────────┘
                           ↓ (merged into)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Methodology (02_methodology_python.yml)                │
│   - Language-specific standards (Python/Java/etc.)               │
│   - Framework requirements                                       │
│   - Testing frameworks                                           │
└─────────────────────────────────────────────────────────────────┘
                           ↓ (merged into)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Project-Specific (03_project_payment_gateway.yml)      │
│   - Project-specific overrides                                   │
│   - PCI compliance requirements                                  │
│   - Stricter coverage (95% vs 80%)                               │
└─────────────────────────────────────────────────────────────────┘
                           ↓ (merged into)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Persona Override (runtime, in memory)                  │
│   - Role-specific view of the project                            │
│   - Security focus areas                                         │
│   - Additional testing requirements (SAST, DAST, penetration)    │
└─────────────────────────────────────────────────────────────────┘
                           ↓ (results in)
┌─────────────────────────────────────────────────────────────────┐
│              MATERIALIZED CONTEXT                                │
│    The final merged configuration visible to Claude              │
└─────────────────────────────────────────────────────────────────┘

KEY INSIGHT:
This is the "transparent memory merge" - Claude receives the FINAL
merged configuration via MCP. No files are written to disk. The merge
happens in memory and is "rehydrated" through the MCP protocol into
Claude's context.

The /show-full-context command lets you inspect this entire state,
see which layers are active, and verify the materialized configuration.
""")

    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
