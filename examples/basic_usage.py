#!/usr/bin/env python3
"""
Basic usage example for AI_SDLC_Context

This demonstrates:
1. Loading multiple configuration files
2. Merging with priority (development overrides base)
3. Accessing values using dot notation
4. Resolving URI references to content
"""
import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_sdlc_config import ConfigManager


def main():
    print("=== AI_SDLC_Context Basic Usage Example ===\n")

    # Create config manager with base path for resolving file:// URIs
    examples_dir = Path(__file__).parent
    manager = ConfigManager(base_path=examples_dir)

    # Load base configuration (lowest priority)
    print("1. Loading base configuration...")
    manager.load_hierarchy("configs/base.yml")
    print("   ✓ Loaded base.yml\n")

    # Load environment-specific configuration (higher priority)
    print("2. Loading development configuration...")
    manager.load_hierarchy("configs/development.yml")
    print("   ✓ Loaded development.yml\n")

    # Add runtime overrides (highest priority)
    print("3. Adding runtime overrides...")
    manager.add_runtime_overrides({
        "llm.agents.discovery.temperature": 0.5,
        "system.session_id": "demo-12345"
    })
    print("   ✓ Added runtime overrides\n")

    # Merge all configurations
    print("4. Merging configurations...")
    manager.merge()
    print("   ✓ Merged 3 configuration layers\n")

    print("=" * 60)
    print("MERGED CONFIGURATION RESULTS")
    print("=" * 60)

    # Access values using dot notation
    print("\n--- Direct Values ---")
    print(f"System Name: {manager.get_value('system.name')}")
    print(f"System Environment: {manager.get_value('system.environment')}")
    print(f"Session ID: {manager.get_value('system.session_id')}")
    print(f"Default Provider: {manager.get_value('llm.default_provider')}")

    # Show priority override example
    print("\n--- Priority Override Example ---")
    print("Discovery agent model (dev overrides base):")
    print(f"  Model: {manager.get_value('llm.agents.discovery.model')}")
    print(f"  Temperature: {manager.get_value('llm.agents.discovery.temperature')}")
    print("  (Temperature was overridden by runtime config)")

    # Access URI references
    print("\n--- URI References ---")
    discovery_uri = manager.get_uri('llm.agents.discovery.prompt')
    print(f"Discovery prompt URI: {discovery_uri}")

    coder_uri = manager.get_uri('llm.agents.coder.prompt')
    print(f"Coder prompt URI: {coder_uri}")

    # Resolve URI to get content
    print("\n--- Resolved URI Content ---")
    print("Discovery agent prompt (first 200 chars):")
    discovery_prompt = manager.get_content('llm.agents.discovery.prompt')
    if discovery_prompt:
        print(f"  {discovery_prompt[:200]}...")
    else:
        print("  [Content not found]")

    # Wildcard search
    print("\n--- Wildcard Search ---")
    print("All agent configurations:")
    agents = manager.find_all('llm.agents.*')
    for path, node in agents:
        model = node.get_value_by_path('model')
        print(f"  {path}: model={model}")

    # Show full hierarchy structure
    print("\n--- Configuration Structure ---")
    print("System section:")
    system_dict = manager.get_node('system').to_dict()
    import json
    print(json.dumps(system_dict, indent=2))

    print("\n✅ Demo complete!")


if __name__ == "__main__":
    main()
