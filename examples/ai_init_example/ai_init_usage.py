#!/usr/bin/env python3
"""
AI Init Example - Using AI_SDLC_Context with ai_init structure

This demonstrates how the ai_init project structure can use
AI_SDLC_Context for flexible, URI-based configuration management.

Key concepts:
1. Configuration layers (base, environment, runtime)
2. URI references to documentation
3. Dot hierarchy for accessing nested config
4. Environment-specific behavior
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ai_sdlc_config import ConfigManager


def main():
    print("=" * 70)
    print("AI Init + AI_SDLC_Context Integration Example")
    print("=" * 70)
    print()

    # Set base path to the example directory
    example_dir = Path(__file__).parent
    config_manager = ConfigManager(base_path=example_dir)

    # Load configuration layers
    print("📁 Loading configuration layers...")
    print("   1. Base configuration (defaults)")
    config_manager.load_hierarchy("configs/base.yml")

    print("   2. Development environment overrides")
    config_manager.load_hierarchy("configs/development.yml")

    print("   3. Runtime overrides (highest priority)")
    config_manager.add_runtime_overrides({
        "project.session_id": "demo-2024-10-15",
        "setup.force_overwrite": True,
        "workflow.min_coverage": 85
    })

    print("\n🔀 Merging configurations...")
    config_manager.merge()
    print("   ✓ Merged 3 configuration layers\n")

    # Show project info
    print("=" * 70)
    print("PROJECT INFORMATION")
    print("=" * 70)
    name = config_manager.get_value("project.name")
    version = config_manager.get_value("project.version")
    env = config_manager.get_value("project.environment")
    debug = config_manager.get_value("project.debug_mode")

    print(f"Project: {name} v{version}")
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Session ID: {config_manager.get_value('project.session_id')}")

    # Show principles
    print("\n" + "=" * 70)
    print("DEVELOPMENT PRINCIPLES (7 Core Principles)")
    print("=" * 70)
    principles = config_manager.find_all("principles.*")
    for path, node in sorted(principles, key=lambda x: x[1].get_value_by_path("priority") or 999):
        priority = node.get_value_by_path("priority")
        name = node.get_value_by_path("name")
        desc = node.get_value_by_path("description")
        print(f"{priority}. {name}")
        print(f"   {desc}")

    # Show BDD principles
    print("\n" + "=" * 70)
    print("BDD PRINCIPLES")
    print("=" * 70)
    bdd_principles = config_manager.find_all("bdd.*")
    for path, node in bdd_principles:
        principle_name = path.split(".")[-1].replace("_", " ").title()
        enabled = node.get_value_by_path("enabled")
        desc = node.get_value_by_path("description")
        status = "✓" if enabled else "✗"
        print(f"{status} {principle_name}: {desc}")

    # Show methodology files (URI references)
    print("\n" + "=" * 70)
    print("METHODOLOGY DOCUMENTATION (URI References)")
    print("=" * 70)
    methodology = config_manager.find_all("methodology.*")
    for path, node in methodology:
        doc_name = path.split(".")[-1].replace("_", " ").title()
        uri = config_manager.get_uri(path)
        print(f"📄 {doc_name}")
        print(f"   URI: {uri}")
        # Show first 100 chars of content
        content = config_manager.get_content(path)
        if content:
            preview = content[:100].replace("\n", " ")
            print(f"   Preview: {preview}...")

    # Show installation components
    print("\n" + "=" * 70)
    print("INSTALLATION COMPONENTS")
    print("=" * 70)
    components = config_manager.find_all("installation.components.*")
    for path, node in components:
        component_name = path.split(".")[-1].replace("_", " ").title()
        enabled = node.get_value_by_path("enabled")
        desc = node.get_value_by_path("description")
        status = "✓ Enabled" if enabled else "✗ Disabled"
        print(f"{status}: {component_name}")
        print(f"         {desc}")

    # Show setup configuration
    print("\n" + "=" * 70)
    print("SETUP CONFIGURATION (with overrides)")
    print("=" * 70)
    setup_config = {
        "Default Target": config_manager.get_value("setup.default_target"),
        "Force Overwrite": config_manager.get_value("setup.force_overwrite"),
        "Update .gitignore": config_manager.get_value("setup.update_gitignore"),
        "Verbose Mode": config_manager.get_value("setup.verbose")
    }
    for key, value in setup_config.items():
        print(f"  {key}: {value}")

    # Show workflow configuration
    print("\n" + "=" * 70)
    print("WORKFLOW CONFIGURATION")
    print("=" * 70)
    workflow_config = {
        "Auto Run Tests": config_manager.get_value("workflow.auto_run_tests"),
        "Generate Coverage": config_manager.get_value("workflow.generate_coverage"),
        "Min Coverage": config_manager.get_value("workflow.min_coverage")
    }
    for key, value in workflow_config.items():
        print(f"  {key}: {value}")

    # Show URLs
    print("\n" + "=" * 70)
    print("EXTERNAL REFERENCES")
    print("=" * 70)
    github = config_manager.get_value("urls.github")
    installer = config_manager.get_value("urls.installer_raw")
    print(f"GitHub Repository: {github}")
    print(f"Installer URL: {installer}")

    # Demonstrate accessing BDD process document
    print("\n" + "=" * 70)
    print("RESOLVED DOCUMENTATION EXAMPLE")
    print("=" * 70)
    print("BDD Process (first 300 characters):")
    bdd_content = config_manager.get_content("methodology.bdd_process")
    if bdd_content:
        print(bdd_content[:300])
        print("...")

    # Show git commit template
    print("\n" + "=" * 70)
    print("GIT COMMIT TEMPLATE")
    print("=" * 70)
    template = config_manager.get_value("git.commit_template")
    print(template)

    # Summary
    print("\n" + "=" * 70)
    print("CONFIGURATION SUMMARY")
    print("=" * 70)
    print(f"Total configuration nodes: {len(list(config_manager.find_all('*')))}")
    print(f"URI references resolved: {len(methodology)}")
    print(f"Active principles: {len(principles)}")
    print(f"Installation components: {len(components)}")

    print("\n✅ Demo complete!")
    print("\nKey Takeaways:")
    print("  • Configuration is layered (base < environment < runtime)")
    print("  • Documentation lives at URIs (file://, https://)")
    print("  • Access via dot notation (e.g., 'principles.test_driven.name')")
    print("  • Wildcard searches supported (e.g., 'principles.*')")
    print("  • URI content loaded lazily and cached")


if __name__ == "__main__":
    main()
