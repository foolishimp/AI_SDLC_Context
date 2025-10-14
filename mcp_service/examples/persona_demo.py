#!/usr/bin/env python3
"""
Persona-Based Context Management Demo

Shows how different team roles (personas) see and interact with
the same project configuration in different ways.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager
from mcp_service.server.persona_manager import PersonaManager


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def simulate_persona_session():
    """Simulate Claude using different personas."""

    # Initialize
    repo_path = Path.cwd() / "example_projects_repo"
    personas_path = Path.cwd() / "personas"

    repo = ProjectRepository(repo_path)
    context_mgr = ContextManager(repo)
    persona_mgr = PersonaManager(personas_path)

    print_section("PERSONA-BASED CONTEXT MANAGEMENT DEMO")
    print("Simulating how different team roles view the same project\n")

    # Load base project context
    project_name = "payment_gateway"
    base_context = context_mgr.load_context(project_name)

    print(f"📦 Base Project: {project_name}")
    print(f"   Classification: {base_context['project'].get('classification')}")
    print(f"   PCI Compliant: {base_context['project'].get('pci_compliant')}")
    print(f"   Min Coverage: {base_context['requirements']['testing']['min_coverage']}%")
    print()

    # ==========================================================================
    # PERSONA 1: Business Analyst
    # ==========================================================================
    print_section("👔 BUSINESS ANALYST VIEW")

    ba_persona = persona_mgr.load_persona("business_analyst")
    ba_context = persona_mgr.apply_persona_to_context(base_context, ba_persona)

    print("\n🎯 Focus Areas:")
    for focus in ba_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("business_analyst")
    for item in checklist:
        print(f"   □ {item}")

    print("\n🔧 Preferred Tools:")
    for tool in ba_persona['persona']['tools']['preferred']:
        print(f"   • {tool}")

    print("\n💡 Claude's Perspective (as BA):")
    print("   When reviewing code, I focus on:")
    print("   - Does this implement the business requirements?")
    print("   - Are acceptance criteria met?")
    print("   - Is the business logic correct?")
    print("   - Technical implementation details are hidden")

    # ==========================================================================
    # PERSONA 2: Software Engineer
    # ==========================================================================
    print_section("💻 SOFTWARE ENGINEER VIEW")

    se_persona = persona_mgr.load_persona("software_engineer")
    se_context = persona_mgr.apply_persona_to_context(base_context, se_persona)

    print("\n🎯 Focus Areas:")
    for focus in se_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("software_engineer")
    for item in checklist:
        print(f"   □ {item}")

    # Show overridden testing requirements
    se_testing = se_context.get('methodology', {}).get('testing', {})
    print("\n📊 Testing Requirements (Engineer's View):")
    print(f"   • TDD Approach: {se_testing.get('tdd_approach')}")
    print(f"   • Unit Coverage: {se_testing.get('coverage_by_type', {}).get('unit')}%")
    print(f"   • Integration Coverage: {se_testing.get('coverage_by_type', {}).get('integration')}%")

    print("\n💡 Claude's Perspective (as Engineer):")
    print("   When reviewing code, I focus on:")
    print("   - Code quality and clean code principles")
    print("   - Unit test coverage")
    print("   - Technical implementation details")
    print("   - Design patterns and SOLID principles")

    # ==========================================================================
    # PERSONA 3: QA Engineer
    # ==========================================================================
    print_section("🧪 QA ENGINEER VIEW")

    qa_persona = persona_mgr.load_persona("qa_engineer")
    qa_context = persona_mgr.apply_persona_to_context(base_context, qa_persona)

    print("\n🎯 Focus Areas:")
    for focus in qa_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("qa_engineer")
    for item in checklist:
        print(f"   □ {item}")

    # Show QA-specific testing requirements
    qa_testing = qa_context.get('methodology', {}).get('testing', {})
    print("\n📊 Testing Requirements (QA's View):")
    print("   Testing Levels Required:")
    for level in qa_testing.get('testing_levels', []):
        print(f"      • {level.replace('_', ' ').title()}")

    print(f"\n   Automation Coverage: {qa_testing.get('automation', {}).get('min_automation_coverage')}%")

    print("\n💡 Claude's Perspective (as QA):")
    print("   When reviewing code, I focus on:")
    print("   - Test coverage across all levels")
    print("   - Edge cases and error scenarios")
    print("   - Test automation")
    print("   - Quality gates")

    # ==========================================================================
    # PERSONA 4: Data Architect
    # ==========================================================================
    print_section("🗄️  DATA ARCHITECT VIEW")

    da_persona = persona_mgr.load_persona("data_architect")
    da_context = persona_mgr.apply_persona_to_context(base_context, da_persona)

    print("\n🎯 Focus Areas:")
    for focus in da_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("data_architect")
    for item in checklist:
        print(f"   □ {item}")

    # Show data-specific requirements
    da_data = da_context.get('methodology', {}).get('data', {})
    print("\n📊 Data Requirements:")
    print("   Mandatory Artifacts:")
    for artifact in da_data.get('mandatory_artifacts', []):
        print(f"      • {artifact.replace('_', ' ').title()}")

    print(f"\n   Normalization: {da_data.get('modeling', {}).get('normalization')}")
    print(f"   Data Validation: {da_data.get('quality', {}).get('data_validation')}")

    print("\n💡 Claude's Perspective (as Data Architect):")
    print("   When reviewing code, I focus on:")
    print("   - Data model design and normalization")
    print("   - Schema documentation")
    print("   - Migration strategies")
    print("   - Performance optimization")

    # ==========================================================================
    # PERSONA 5: Security Engineer
    # ==========================================================================
    print_section("🔒 SECURITY ENGINEER VIEW")

    sec_persona = persona_mgr.load_persona("security_engineer")
    sec_context = persona_mgr.apply_persona_to_context(base_context, sec_persona)

    print("\n🎯 Focus Areas:")
    for focus in sec_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("security_engineer")
    for item in checklist:
        print(f"   □ {item}")

    # Show security-specific requirements (overridden)
    sec_security = sec_context.get('methodology', {}).get('security', {})
    print("\n📊 Security Requirements (Security Engineer's View):")
    print("   Testing Types Required:")
    for test_type in sec_security.get('testing', {}).get('required_types', []):
        print(f"      • {test_type.upper()}")

    vuln_mgmt = sec_security.get('vulnerability_management', {})
    print(f"\n   Scan Frequency: {vuln_mgmt.get('scan_frequency')}")
    print(f"   Critical Fix SLA: {vuln_mgmt.get('critical_fix_sla_hours')} hours")

    print("\n💡 Claude's Perspective (as Security Engineer):")
    print("   When reviewing code, I focus on:")
    print("   - Security vulnerabilities")
    print("   - Authentication and authorization")
    print("   - Data encryption")
    print("   - Compliance with security frameworks")

    # ==========================================================================
    # PERSONA 6: DevOps Engineer
    # ==========================================================================
    print_section("🚀 DEVOPS ENGINEER VIEW")

    devops_persona = persona_mgr.load_persona("devops_engineer")
    devops_context = persona_mgr.apply_persona_to_context(base_context, devops_persona)

    print("\n🎯 Focus Areas:")
    for focus in devops_context['active_persona']['focus_areas']:
        print(f"   • {focus}")

    print("\n📋 Review Checklist:")
    checklist = persona_mgr.get_persona_review_checklist("devops_engineer")
    for item in checklist:
        print(f"   □ {item}")

    # Show DevOps-specific requirements
    devops_deploy = devops_context.get('methodology', {}).get('deployment', {})
    print("\n📊 Deployment Requirements:")
    print("   Mandatory Artifacts:")
    for artifact in devops_deploy.get('mandatory_artifacts', []):
        print(f"      • {artifact.replace('_', ' ').title()}")

    ci_cd = devops_deploy.get('ci_cd', {})
    print(f"\n   Deployment Strategy: {ci_cd.get('deployment_strategy', 'N/A')}")
    print(f"   Rollback Automated: {ci_cd.get('rollback_automated', False)}")

    print("\n💡 Claude's Perspective (as DevOps Engineer):")
    print("   When reviewing code, I focus on:")
    print("   - Deployment procedures")
    print("   - Infrastructure as code")
    print("   - Monitoring and observability")
    print("   - Rollback capabilities")

    # ==========================================================================
    # COMPARISON
    # ==========================================================================
    print_section("📊 PERSONA COMPARISON")

    print("\nSame Project, Different Perspectives:\n")

    personas_reviewed = [
        ("Business Analyst", "Requirements & acceptance criteria"),
        ("Software Engineer", "Code quality & unit tests"),
        ("QA Engineer", "Test coverage & quality gates"),
        ("Data Architect", "Data model & schema"),
        ("Security Engineer", "Security vulnerabilities & compliance"),
        ("DevOps Engineer", "Deployment & infrastructure")
    ]

    print(f"{'Persona':<25} {'Primary Focus':<40}")
    print("-" * 65)
    for persona, focus in personas_reviewed:
        print(f"{persona:<25} {focus:<40}")

    # ==========================================================================
    # PERSONA SWITCHING
    # ==========================================================================
    print_section("🔄 PERSONA SWITCHING")

    print("\n📝 User: Switch from software_engineer to qa_engineer\n")

    switch_result = persona_mgr.switch_persona("software_engineer", "qa_engineer")

    print("🤖 Claude: Switching personas...\n")
    print(f"   From: {switch_result['from']}")
    print(f"   To: {switch_result['to']}")

    if 'focus_changed' in switch_result:
        print("\n   Focus Areas Changed:")
        if switch_result['focus_changed']['added_focus']:
            print("   Added:")
            for focus in switch_result['focus_changed']['added_focus']:
                print(f"      ✚ {focus}")
        if switch_result['focus_changed']['removed_focus']:
            print("   Removed:")
            for focus in switch_result['focus_changed']['removed_focus']:
                print(f"      ✖ {focus}")

    # ==========================================================================
    # LIST AVAILABLE PERSONAS
    # ==========================================================================
    print_section("📋 AVAILABLE PERSONAS")

    personas_list = persona_mgr.list_personas()
    print(f"\nTotal Personas Available: {len(personas_list)}\n")

    for persona in personas_list:
        print(f"👤 {persona['name']} ({persona['role']})")
        print(f"   Focus: {', '.join(persona['focus_areas'][:3])}...")
        print()

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================
    print_section("✅ PERSONA-BASED CONTEXT MANAGEMENT DEMONSTRATED")

    print("""
What you just saw:

1. 👔 Business Analyst View
   • Hides technical details
   • Focuses on requirements and business logic
   • Tools: JIRA, Confluence, Lucidchart

2. 💻 Software Engineer View
   • Full technical details
   • Emphasizes code quality and testing
   • Tools: VSCode, Git, pytest, mypy

3. 🧪 QA Engineer View
   • Focuses on test coverage and quality gates
   • Multiple testing levels required
   • Tools: pytest, Selenium, JMeter

4. 🗄️  Data Architect View
   • Data model and schema focus
   • Mandatory ERD and migrations
   • Tools: DBVisualizer, Liquibase, dbt

5. 🔒 Security Engineer View
   • Security vulnerabilities and compliance
   • Continuous scanning required
   • Tools: Snyk, OWASP ZAP, Burp Suite

6. 🚀 DevOps Engineer View
   • Deployment and infrastructure
   • IaC and monitoring required
   • Tools: Terraform, Kubernetes, Prometheus

🎯 Key Insight:
   Same project, but each persona sees what matters for THEIR ROLE!
   Claude adapts its perspective and recommendations based on persona.

🎭 This enables Claude to act as ANY team member!
    """)


if __name__ == "__main__":
    simulate_persona_session()
