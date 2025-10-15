#!/usr/bin/env python3
"""
Example: Loading Methodology Context for a New Project

This demonstrates how to:
1. Load the ai_init_methodology as a base context
2. Add language-specific context (Python)
3. Add architecture patterns
4. Merge into a project-specific configuration

Use case: Starting a new Python project with Sacred Seven methodology
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_sdlc_config import ConfigManager


def main():
    print("=" * 80)
    print("Loading Methodology Context Example")
    print("=" * 80)
    print()

    # Setup paths
    projects_repo = Path(__file__).parent.parent / "example_projects_repo"
    manager = ConfigManager(base_path=projects_repo)

    print("Step 1: Load Base Methodology (ai_init)")
    print("-" * 80)
    print("Loading: ai_init_methodology")
    print("  Contains: Sacred Seven principles, TDD workflow")
    manager.load_hierarchy("ai_init_methodology/config/config.yml")
    print("  ✓ Loaded")
    print()

    print("Step 2: Add Language-Specific Standards (Python)")
    print("-" * 80)
    print("Loading: python_standards")
    print("  Contains: PEP 8, pytest, type checking, linting")
    manager.load_hierarchy("python_standards/config/config.yml")
    print("  ✓ Loaded")
    print()

    print("Step 3: Add Corporate Policies (Optional)")
    print("-" * 80)
    print("Loading: acme_corporate")
    print("  Contains: Security requirements, review policies")
    manager.load_hierarchy("acme_corporate/config/config.yml")
    print("  ✓ Loaded")
    print()

    print("Step 4: Add Project-Specific Overrides")
    print("-" * 80)
    print("Adding runtime overrides for this specific project...")
    manager.add_runtime_overrides({
        "project.name": "my_new_project",
        "project.type": "api_service",
        "project.risk_level": "medium"
    })
    print("  ✓ Added")
    print()

    print("Step 5: Merge All Contexts")
    print("-" * 80)
    print("Merging layers (lowest → highest priority):")
    print("  1. ai_init_methodology (foundation)")
    print("  2. python_standards (language-specific)")
    print("  3. acme_corporate (organizational)")
    print("  4. runtime overrides (project-specific)")
    manager.merge()
    print("  ✓ Merged")
    print()

    print("=" * 80)
    print("MERGED CONFIGURATION AVAILABLE")
    print("=" * 80)
    print()

    # Show Sacred Seven Principles
    print("📋 Sacred Seven Principles")
    print("-" * 80)
    principles = manager.find_all("methodology.principles.*")
    for path, node in principles:
        if node.is_leaf() and not path.endswith(("_uri", "principle", "requirements")):
            mantra = node.get_value_by_path("mantra")
            if mantra:
                print(f"  {path.split('.')[-1]}: {mantra}")
    print()

    # Show TDD Cycle
    print("🔄 TDD Workflow")
    print("-" * 80)
    tdd_cycle = manager.get_node("methodology.processes.tdd_workflow.cycle")
    if tdd_cycle and tdd_cycle.is_container():
        for idx, phase_node in tdd_cycle.children.items():
            phase = phase_node.get_value_by_path("phase")
            action = phase_node.get_value_by_path("action")
            if phase and action:
                print(f"  {phase}: {action}")
    print()

    # Show Quality Standards
    print("⚡ Quality Standards")
    print("-" * 80)
    coverage = manager.get_value("methodology.quality_standards.testing.coverage_minimum")
    print(f"  Test Coverage: >{coverage}%")

    type_hints = manager.get_value("methodology.quality_standards.code.type_hints")
    print(f"  Type Hints: {type_hints}")

    style = manager.get_value("methodology.quality_standards.code.style_guide")
    print(f"  Style Guide: {style}")
    print()

    # Show Coding Standards (from Python)
    print("🐍 Python-Specific Standards")
    print("-" * 80)
    formatter = manager.get_value("methodology.coding.standards.formatter")
    print(f"  Formatter: {formatter}")

    linting_tools = manager.get_value("methodology.coding.linting.tools")
    if linting_tools:
        print(f"  Linting: {', '.join(linting_tools)}")

    test_framework = manager.get_value("methodology.testing.framework")
    print(f"  Testing: {test_framework}")
    print()

    # Show Corporate Requirements (if loaded)
    security = manager.get_value("sdlc.security.requirements.encryption_at_rest")
    if security is not None:
        print("🔒 Corporate Security Requirements")
        print("-" * 80)
        print(f"  Encryption at Rest: {security}")

        mfa = manager.get_value("sdlc.security.requirements.mfa_required")
        print(f"  MFA Required: {mfa}")
        print()

    # Show Decision Framework
    print("❓ Before You Code - Decision Framework")
    print("-" * 80)
    questions = manager.get_node("methodology.decision_framework.before_coding")
    if questions and questions.is_container():
        for idx, q_node in questions.children.items():
            question = q_node.get_value_by_path("question")
            principle = q_node.get_value_by_path("principle")
            if question:
                print(f"  {principle}. {question}")
    print()

    # Show Ultimate Mantra
    print("🔥 Ultimate Mantra")
    print("-" * 80)
    mantra = manager.get_value("mantras.ultimate")
    print(f"  {mantra}")
    print()

    print("=" * 80)
    print("✅ Configuration Ready for New Project!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Use merged config to initialize project")
    print("  2. Follow Sacred Seven principles")
    print("  3. Apply TDD workflow (RED→GREEN→REFACTOR)")
    print("  4. Maintain quality standards")
    print()
    print("To access via MCP:")
    print("  1. Start MCP service: python -m server.main")
    print("  2. Use get_project tool: project_id='ai_init_methodology'")
    print("  3. Use merge_projects tool to combine contexts")
    print()


if __name__ == "__main__":
    main()
