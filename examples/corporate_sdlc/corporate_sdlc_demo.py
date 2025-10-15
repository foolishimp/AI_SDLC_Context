#!/usr/bin/env python3
"""
Corporate SDLC Multi-Layer Configuration Demo

This demonstrates how a corporate developer can use AI_SDLC_Context
to manage multi-layered SDLC configurations:

Layer 1: Corporate Base (policies, standards)
Layer 2: Methodology (language/framework specific)
Layer 3: Project-Specific (overrides per project)
Layer 4: Runtime (environment, user overrides)

Usage:
    python corporate_sdlc_demo.py payment_service  # High-security project
    python corporate_sdlc_demo.py internal_dashboard  # Internal tool
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ai_sdlc_config import ConfigManager


def load_project_config(project_name: str, environment: str = "development"):
    """
    Load multi-layer configuration for a specific project.

    Args:
        project_name: Name of the project (payment_service, internal_dashboard)
        environment: Environment (development, staging, production)

    Returns:
        ConfigManager with merged configuration
    """
    example_dir = Path(__file__).parent
    manager = ConfigManager(base_path=example_dir)

    print(f"Loading configuration for project: {project_name}")
    print(f"Environment: {environment}\n")

    # Layer 1: Corporate Base (mandatory for all projects)
    print("📋 Layer 1: Corporate Base")
    print("   Loading corporate policies and standards...")
    manager.load_hierarchy("configs/corporate/base.yml")

    # Layer 2: Methodology (language-specific)
    # Determine from project config or convention
    if project_name == "payment_service":
        print("📋 Layer 2: Python Methodology")
        print("   Loading Python coding standards...")
        manager.load_hierarchy("configs/methodology/python_standards.yml")
    elif project_name == "internal_dashboard":
        print("📋 Layer 2: JavaScript Methodology")
        print("   Loading JavaScript/TypeScript standards...")
        manager.load_hierarchy("configs/methodology/javascript_standards.yml")

    # Layer 3: Project-Specific
    print(f"📋 Layer 3: Project '{project_name}'")
    print("   Loading project-specific overrides...")
    manager.load_hierarchy(f"configs/projects/{project_name}.yml")

    # Layer 4: Runtime (environment, user preferences)
    print(f"📋 Layer 4: Runtime ({environment})")
    print("   Applying runtime overrides...\n")

    runtime_overrides = {
        "environment": environment,
        "runtime.user": "john.doe@acme.com",
        "runtime.workstation": "DEV-LAPTOP-001"
    }

    if environment == "production":
        runtime_overrides.update({
            "security.vulnerability_management.scan_frequency": "continuous",
            "quality.gates.code_quality.max_critical_issues": 0
        })

    manager.add_runtime_overrides(runtime_overrides)

    # Merge all layers
    print("🔀 Merging all configuration layers...")
    manager.merge()
    print("   ✓ Configuration merged successfully\n")

    return manager


def display_project_config(config: ConfigManager, project_name: str):
    """Display key configuration values for a project."""

    print("=" * 80)
    print(f"CONFIGURATION FOR: {config.get_value('project.name')}")
    print("=" * 80)

    # Project Info
    print("\n📦 PROJECT INFORMATION")
    print(f"   Code: {config.get_value('project.code')}")
    print(f"   Team: {config.get_value('project.team')}")
    print(f"   Tech Lead: {config.get_value('project.tech_lead')}")
    print(f"   Classification: {config.get_value('project.classification')}")
    if config.get_value('project.pci_compliant'):
        print(f"   ⚠️  PCI Compliant: YES")

    # Corporate Policies
    print("\n📜 CORPORATE POLICIES (URI References)")
    policies = config.find_all("corporate.policies.*")
    for path, node in policies:
        policy_name = path.split(".")[-1].replace("_", " ").title()
        uri = node.get_value_by_path("uri")
        version = node.get_value_by_path("version")
        mandatory = node.get_value_by_path("mandatory")
        status = "⚠️  MANDATORY" if mandatory else "Optional"
        print(f"   {policy_name} v{version} - {status}")
        print(f"      URI: {uri}")

    # Coding Standards
    print("\n💻 CODING STANDARDS")
    standards = config.get_value("methodology.coding.standards")
    if standards:
        for key, value in standards.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")

    required_practices = config.get_value("methodology.coding.required_practices")
    if required_practices:
        print("\n   Required Practices:")
        for practice in required_practices:
            print(f"      ✓ {practice}")

    # Testing Requirements
    print("\n🧪 TESTING REQUIREMENTS")
    min_coverage = config.get_value("methodology.testing.min_coverage")
    print(f"   Minimum Coverage: {min_coverage}%")

    test_types = config.get_value("methodology.testing.required_types")
    if test_types:
        print("   Required Test Types:")
        for test_type in test_types:
            print(f"      • {test_type.replace('_', ' ').title()}")

    # Quality Gates
    print("\n🚦 QUALITY GATES")
    quality_gates = config.get_value("quality.gates.code_quality")
    if quality_gates:
        print("   Code Quality:")
        print(f"      Min Coverage: {quality_gates.get('min_test_coverage')}%")
        print(f"      Max Code Smells: {quality_gates.get('max_code_smells')}")
        print(f"      Max Critical Issues: {quality_gates.get('max_critical_issues')}")
        print(f"      Max High Issues: {quality_gates.get('max_high_issues')}")

    # Security Requirements
    print("\n🔒 SECURITY REQUIREMENTS")
    vuln_mgmt = config.get_value("security.vulnerability_management")
    if vuln_mgmt:
        print(f"   Scan Frequency: {vuln_mgmt.get('scan_frequency')}")
        print(f"   Critical Fix SLA: {vuln_mgmt.get('critical_fix_sla_hours')} hours")
        print(f"   High Fix SLA: {vuln_mgmt.get('high_fix_sla_hours')} hours")

    # Deployment Approval Chain
    print("\n🚀 DEPLOYMENT APPROVAL CHAIN")
    approval_chain = config.get_value("methodology.deployment.approval_chain")
    if approval_chain:
        for env, approvers in approval_chain.items():
            print(f"   {env.title()}:")
            for approver in approvers:
                print(f"      → {approver.replace('_', ' ').title()}")

    # Compliance
    print("\n📋 COMPLIANCE FRAMEWORKS")
    frameworks = config.get_value("compliance.frameworks")
    if frameworks:
        for framework in frameworks:
            print(f"   ✓ {framework}")

    # Project-Specific Documentation
    print("\n📚 PROJECT DOCUMENTATION")
    project_docs = config.find_all(f"projects.{project_name.replace('-', '_')}.docs.*")
    if project_docs:
        for path, node in project_docs:
            doc_type = path.split(".")[-1].replace("_", " ").title()
            uri = config.get_uri(path)
            print(f"   {doc_type}: {uri}")

    # Tools
    print("\n🔧 TOOLS & FRAMEWORKS")
    if project_name == "payment_service":
        print("   Language: Python")
        print(f"   Package Manager: {config.get_value('tools.package_management.tool')}")
        print(f"   Testing: {config.get_value('methodology.testing.framework')}")
    elif project_name == "internal_dashboard":
        print("   Language: JavaScript/TypeScript")
        print(f"   Frontend Framework: {config.get_value('tools.frontend.framework')}")
        print(f"   Bundler: {config.get_value('tools.frontend.bundler')}")
        print(f"   Package Manager: {config.get_value('tools.frontend.package_manager')}")

    print("\n" + "=" * 80)


def compare_projects(payment_config: ConfigManager, dashboard_config: ConfigManager):
    """Compare configuration differences between two projects."""

    print("\n" + "=" * 80)
    print("COMPARISON: Payment Service vs Internal Dashboard")
    print("=" * 80)

    comparisons = [
        ("Min Test Coverage", "methodology.testing.min_coverage"),
        ("Max Function Lines", "methodology.coding.standards.max_function_lines"),
        ("Max Complexity", "methodology.coding.standards.max_complexity"),
        ("Critical Fix SLA (hours)", "security.vulnerability_management.critical_fix_sla_hours"),
        ("Max Critical Issues", "quality.gates.code_quality.max_critical_issues"),
        ("Max Code Smells", "quality.gates.code_quality.max_code_smells"),
    ]

    print("\n{:<30} {:<20} {:<20}".format("Metric", "Payment Service", "Internal Dashboard"))
    print("-" * 70)

    for label, path in comparisons:
        payment_val = payment_config.get_value(path)
        dashboard_val = dashboard_config.get_value(path)
        print("{:<30} {:<20} {:<20}".format(label, str(payment_val), str(dashboard_val)))

    print("\n💡 Key Differences:")
    print("   • Payment Service has STRICTER requirements (financial/PCI compliance)")
    print("   • Internal Dashboard has RELAXED requirements (internal tool)")
    print("   • Both inherit same corporate policies (security, code review)")
    print("   • Each has language-specific methodology (Python vs JavaScript)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python corporate_sdlc_demo.py <project_name>")
        print("\nAvailable projects:")
        print("  - payment_service")
        print("  - internal_dashboard")
        sys.exit(1)

    project_name = sys.argv[1]
    environment = sys.argv[2] if len(sys.argv) > 2 else "development"

    print("=" * 80)
    print("CORPORATE SDLC MULTI-LAYER CONFIGURATION DEMO")
    print("=" * 80)
    print()

    # Load configuration
    config = load_project_config(project_name, environment)

    # Display configuration
    display_project_config(config, project_name)

    # If we want to compare both projects
    if project_name == "payment_service":
        print("\n\n🔄 Loading Internal Dashboard for comparison...")
        dashboard_config = load_project_config("internal_dashboard", environment)
        compare_projects(config, dashboard_config)

    print("\n✅ Demo complete!")
    print("\nKey Takeaways:")
    print("  • Layer 1 (Corporate): Policies apply to ALL projects")
    print("  • Layer 2 (Methodology): Language/framework specific standards")
    print("  • Layer 3 (Project): Project-specific overrides and requirements")
    print("  • Layer 4 (Runtime): Environment and user-specific settings")
    print("  • Each layer can override previous layers")
    print("  • Critical systems (payments) have stricter requirements")
    print("  • Internal tools can have relaxed requirements")
    print("  • All documentation referenced via URIs (file://, https://)")


if __name__ == "__main__":
    main()
