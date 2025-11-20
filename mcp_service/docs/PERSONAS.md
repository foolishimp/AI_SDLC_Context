# Persona-Based Context Management

## ⚠️ Status: Legacy Documentation

**Note**: This document describes the persona system design. Personas are now implemented as hierarchical projects within `example_projects_repo/` rather than standalone YAML files. Personas can be created as projects and loaded as layers in the merge hierarchy.

For current implementation, personas should be structured as ai_sdlc_method projects with `project.json` and `config/config.yml` files.

---

## Overview

**Personas** add a role-based layer to the context management system, allowing different team members (business analyst, architect, engineer, tester, etc.) to have customized views and overrides of the same project configuration.

## Architecture

### Configuration Layers with Personas

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Persona (Highest Priority)                        │
│   - Role-specific overrides                                 │
│   - Focus areas and priorities                              │
│   - Documentation preferences                               │
│   - Tool configurations                                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Runtime                                            │
│   - Environment (dev/staging/prod)                          │
│   - User preferences                                        │
│   - Dynamic overrides                                       │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Project-Specific                                  │
│   - projects/payment_service.yml                            │
│   - Project requirements                                    │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Methodology                                        │
│   - methodology/python_standards.yml                        │
│   - Language-specific standards                            │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Corporate Base (Lowest Priority)                  │
│   - corporate/base.yml                                      │
│   - Policies, compliance, security                         │
└─────────────────────────────────────────────────────────────┘
```

**Merge Priority**: Layer 5 > Layer 4 > Layer 3 > Layer 2 > Layer 1

---

## Persona Definitions

### Repository Structure

```
personas/
├── business_analyst.yml          # BA persona
├── data_architect.yml             # Data architect persona
├── software_engineer.yml          # Software engineer persona
├── qa_engineer.yml                # QA/tester persona
├── devops_engineer.yml            # DevOps persona
├── security_engineer.yml          # Security persona
├── tech_lead.yml                  # Tech lead persona
└── product_manager.yml            # Product manager persona
```

---

## Example Personas

### Business Analyst

```yaml
# personas/business_analyst.yml
persona:
  name: "Business Analyst"
  role: "business_analyst"
  focus_areas:
    - "Requirements gathering"
    - "User stories"
    - "Acceptance criteria"
    - "Business process modeling"

  preferences:
    documentation:
      style: "narrative"  # vs technical
      detail_level: "high"
      include_diagrams: true
      format: "markdown"

  overrides:
    # Focus on requirements and documentation
    methodology:
      requirements:
        mandatory_artifacts:
          - "user_stories"
          - "acceptance_criteria"
          - "process_flows"
          - "data_dictionary"
        documentation_templates:
          user_story: "file://personas/templates/user_story.md"
          acceptance_criteria: "file://personas/templates/acceptance_criteria.md"

    # Less technical detail needed
    coding:
      show_implementation_details: false
      focus_on: "business_logic"

  tools:
    preferred:
      - "JIRA"
      - "Confluence"
      - "Lucidchart"
      - "Excel"

  prompts:
    code_review_focus:
      - "Does this meet business requirements?"
      - "Are acceptance criteria satisfied?"
      - "Is the business logic correct?"

    documentation_focus:
      - "User-facing documentation"
      - "Business process flows"
      - "Data definitions"

  notifications:
    interested_in:
      - "requirement_changes"
      - "acceptance_criteria_updates"
      - "business_logic_changes"
```

---

### Data Architect

```yaml
# personas/data_architect.yml
persona:
  name: "Data Architect"
  role: "data_architect"
  focus_areas:
    - "Data modeling"
    - "Database design"
    - "Data governance"
    - "Performance optimization"

  preferences:
    documentation:
      style: "technical"
      include_schemas: true
      include_erd: true

  overrides:
    methodology:
      data:
        mandatory_artifacts:
          - "erd_diagram"
          - "schema_documentation"
          - "data_dictionary"
          - "migration_scripts"

        modeling:
          normalization: "3NF"  # vs denormalized
          naming_convention: "snake_case"

        quality:
          data_validation: "strict"
          referential_integrity: "enforced"

        performance:
          indexing_strategy: "documented"
          query_optimization: "required"

    # More stringent data requirements
    testing:
      required_types:
        - "data_integrity"
        - "performance"
        - "migration"
        - "backup_restore"

  tools:
    preferred:
      - "DBVisualizer"
      - "Liquibase"
      - "dbt"
      - "SQL Developer"

  prompts:
    code_review_focus:
      - "Is the data model normalized?"
      - "Are indexes defined properly?"
      - "Is referential integrity maintained?"
      - "Are migrations reversible?"

    documentation_focus:
      - "Schema documentation"
      - "Data dictionaries"
      - "ERD diagrams"
      - "Migration strategies"

  notifications:
    interested_in:
      - "schema_changes"
      - "data_model_updates"
      - "migration_events"
      - "performance_issues"
```

---

### Software Engineer

```yaml
# personas/software_engineer.yml
persona:
  name: "Software Engineer"
  role: "software_engineer"
  focus_areas:
    - "Code implementation"
    - "Unit testing"
    - "Code quality"
    - "Technical design"

  preferences:
    documentation:
      style: "technical"
      detail_level: "implementation"
      include_code_examples: true

  overrides:
    methodology:
      coding:
        emphasis:
          - "clean_code"
          - "SOLID_principles"
          - "design_patterns"
          - "code_reusability"

        review_checklist:
          - "Code follows style guide"
          - "Unit tests included"
          - "No code duplication"
          - "Error handling proper"
          - "Performance considered"

      testing:
        focus:
          - "unit"
          - "integration"

        tdd_approach: "red_green_refactor"

        coverage_by_type:
          unit: 90
          integration: 80

  tools:
    preferred:
      - "VSCode"
      - "Git"
      - "pytest"
      - "black"
      - "mypy"

  prompts:
    code_review_focus:
      - "Is the code clean and readable?"
      - "Are there unit tests?"
      - "Is error handling comprehensive?"
      - "Any code smells?"

    documentation_focus:
      - "Code comments"
      - "Function docstrings"
      - "API documentation"
      - "Technical README"

  notifications:
    interested_in:
      - "code_reviews"
      - "build_failures"
      - "test_failures"
      - "code_quality_alerts"
```

---

### QA Engineer / Tester

```yaml
# personas/qa_engineer.yml
persona:
  name: "QA Engineer"
  role: "qa_engineer"
  focus_areas:
    - "Test planning"
    - "Test automation"
    - "Quality assurance"
    - "Bug tracking"

  preferences:
    documentation:
      style: "structured"
      detail_level: "test_scenarios"
      include_test_plans: true

  overrides:
    methodology:
      testing:
        emphasis:
          - "Test coverage"
          - "Test automation"
          - "Regression testing"
          - "Defect prevention"

        mandatory_artifacts:
          - "test_plan"
          - "test_cases"
          - "test_data"
          - "automation_scripts"

        testing_levels:
          - "unit"
          - "integration"
          - "system"
          - "acceptance"
          - "regression"
          - "performance"
          - "security"

        automation:
          framework: "pytest + selenium"
          min_automation_coverage: 80

        quality_gates:
          zero_critical_bugs: true
          zero_high_bugs_in_production: true
          regression_suite_passing: true

  tools:
    preferred:
      - "pytest"
      - "Selenium"
      - "Postman"
      - "JMeter"
      - "JIRA"

  prompts:
    code_review_focus:
      - "Are there adequate tests?"
      - "Are edge cases covered?"
      - "Is test data representative?"
      - "Are tests maintainable?"

    documentation_focus:
      - "Test plans"
      - "Test cases"
      - "Test data requirements"
      - "Bug reproduction steps"

  notifications:
    interested_in:
      - "test_failures"
      - "new_features"
      - "bug_reports"
      - "release_candidates"
```

---

### DevOps Engineer

```yaml
# personas/devops_engineer.yml
persona:
  name: "DevOps Engineer"
  role: "devops_engineer"
  focus_areas:
    - "CI/CD pipelines"
    - "Infrastructure as code"
    - "Monitoring and observability"
    - "Deployment automation"

  preferences:
    documentation:
      style: "operational"
      detail_level: "deployment_procedures"
      include_runbooks: true

  overrides:
    methodology:
      deployment:
        emphasis:
          - "Automation"
          - "Infrastructure as code"
          - "Monitoring"
          - "Rollback procedures"

        mandatory_artifacts:
          - "deployment_pipeline"
          - "infrastructure_code"
          - "monitoring_config"
          - "runbook"
          - "rollback_plan"

        ci_cd:
          automated_tests: "all"
          deployment_strategy: "blue_green"
          rollback_automated: true

        infrastructure:
          iac_tool: "terraform"
          container_platform: "kubernetes"
          monitoring: "prometheus + grafana"

        observability:
          logging: "centralized"
          metrics: "comprehensive"
          tracing: "distributed"
          alerts: "actionable"

  tools:
    preferred:
      - "Jenkins"
      - "GitLab CI"
      - "Terraform"
      - "Kubernetes"
      - "Prometheus"
      - "Grafana"

  prompts:
    code_review_focus:
      - "Is this deployable?"
      - "Are there deployment scripts?"
      - "Is rollback possible?"
      - "Are there monitoring hooks?"

    documentation_focus:
      - "Deployment procedures"
      - "Infrastructure diagrams"
      - "Monitoring setup"
      - "Troubleshooting guides"

  notifications:
    interested_in:
      - "deployment_failures"
      - "infrastructure_changes"
      - "performance_degradation"
      - "security_alerts"
```

---

### Security Engineer

```yaml
# personas/security_engineer.yml
persona:
  name: "Security Engineer"
  role: "security_engineer"
  focus_areas:
    - "Security testing"
    - "Vulnerability management"
    - "Compliance"
    - "Threat modeling"

  preferences:
    documentation:
      style: "security_focused"
      detail_level: "threat_analysis"
      include_threat_models: true

  overrides:
    methodology:
      security:
        emphasis:
          - "Secure by design"
          - "Threat modeling"
          - "Security testing"
          - "Compliance"

        mandatory_artifacts:
          - "threat_model"
          - "security_requirements"
          - "penetration_test_results"
          - "compliance_checklist"

        testing:
          required_types:
            - "sast"  # Static analysis
            - "dast"  # Dynamic analysis
            - "dependency_scan"
            - "penetration"
            - "compliance"

        vulnerability_management:
          scan_frequency: "continuous"
          critical_fix_sla_hours: 4
          high_fix_sla_hours: 24

        compliance:
          frameworks:
            - "OWASP Top 10"
            - "CWE Top 25"
          automated_checks: true

    # Stricter quality gates
    quality:
      gates:
        max_critical_security_issues: 0
        max_high_security_issues: 0

  tools:
    preferred:
      - "Snyk"
      - "OWASP ZAP"
      - "Burp Suite"
      - "SonarQube"
      - "Vault"

  prompts:
    code_review_focus:
      - "Are there security vulnerabilities?"
      - "Is authentication proper?"
      - "Is data encrypted?"
      - "Are inputs validated?"

    documentation_focus:
      - "Threat models"
      - "Security requirements"
      - "Compliance documentation"
      - "Incident response plans"

  notifications:
    interested_in:
      - "security_vulnerabilities"
      - "compliance_violations"
      - "security_incidents"
      - "authentication_failures"
```

---

### Tech Lead

```yaml
# personas/tech_lead.yml
persona:
  name: "Tech Lead"
  role: "tech_lead"
  focus_areas:
    - "Technical architecture"
    - "Team coordination"
    - "Code quality"
    - "Technical decisions"

  preferences:
    documentation:
      style: "comprehensive"
      detail_level: "architecture"
      include_adrs: true  # Architecture Decision Records

  overrides:
    methodology:
      architecture:
        emphasis:
          - "System design"
          - "Technical debt management"
          - "Cross-team coordination"
          - "Quality standards"

        mandatory_artifacts:
          - "architecture_diagram"
          - "technical_decisions"  # ADRs
          - "api_contracts"
          - "integration_points"

        review_gates:
          tech_lead_approval: "required"
          architecture_review: "for_major_changes"

      coding:
        standards_enforcement: "strict"
        code_review_mandatory: true
        pair_programming_encouraged: true

      quality:
        gates:
          all_tests_passing: true
          code_coverage_met: true
          no_critical_issues: true
          documentation_complete: true

  tools:
    preferred:
      - "Confluence"
      - "JIRA"
      - "GitHub"
      - "Slack"
      - "Draw.io"

  prompts:
    code_review_focus:
      - "Does this fit the architecture?"
      - "Is this maintainable?"
      - "Are there better alternatives?"
      - "Does this introduce technical debt?"

    documentation_focus:
      - "Architecture documentation"
      - "Technical decisions (ADRs)"
      - "Team guidelines"
      - "Integration documentation"

  notifications:
    interested_in:
      - "all_major_changes"
      - "architecture_violations"
      - "technical_debt"
      - "cross_team_dependencies"
```

---

## Usage Patterns

### Pattern 1: Persona + Project Context

```python
# Load project context
load_context("payment_gateway")

# Apply persona
load_persona("business_analyst")

# Result: BA view of payment gateway
# - Focuses on requirements and acceptance criteria
# - Hides implementation details
# - Emphasizes business logic
# - Shows relevant documentation
```

### Pattern 2: Switching Personas

```python
# Engineer working on implementation
load_context("payment_gateway")
load_persona("software_engineer")
# → Sees code details, unit tests, technical docs

# Switch to QA for review
switch_persona("software_engineer", "qa_engineer")
# → Sees test coverage, test plans, quality gates
```

### Pattern 3: Multi-Persona Collaboration

```python
# Tech lead reviewing architecture
load_context("payment_gateway")
load_persona("tech_lead")
# → Reviews architecture, technical decisions

# Security engineer reviewing security
load_persona("security_engineer")
# → Reviews threat model, security tests, compliance
```

---

## MCP Tools for Personas

### New Tools

```python
@server.call_tool()
async def load_persona(persona_name: str, project_name: str):
    """
    Load persona configuration and apply to project context.

    Args:
        persona_name: Role (business_analyst, software_engineer, etc.)
        project_name: Project to apply persona to

    Returns:
        Combined project + persona context
    """
    # Load project context
    project_ctx = context_mgr.load_context(project_name)

    # Load persona config
    persona_config = load_persona_config(persona_name)

    # Merge with persona having highest priority
    combined_ctx = merge_contexts(project_ctx, persona_config)

    return combined_ctx


@server.call_tool()
async def switch_persona(from_persona: str, to_persona: str):
    """
    Switch from one persona to another.

    Shows what changed in focus areas and overrides.
    """
    # Load new persona
    new_persona = load_persona_config(to_persona)

    # Show differences
    differences = compare_personas(from_persona, to_persona)

    return {
        "switched_from": from_persona,
        "switched_to": to_persona,
        "focus_changes": differences
    }


@server.call_tool()
async def list_personas():
    """List all available personas."""
    return [
        "business_analyst",
        "data_architect",
        "software_engineer",
        "qa_engineer",
        "devops_engineer",
        "security_engineer",
        "tech_lead",
        "product_manager"
    ]
```

---

## Example: Claude with Persona Context

### Business Analyst View

```
User: Load payment_gateway context with business_analyst persona

Claude: ✓ Loaded payment_gateway (PCI compliant)
        ✓ Applied business_analyst persona

Context Understanding:
• Focus: Requirements, user stories, acceptance criteria
• View: Business logic (implementation details hidden)
• Documentation: Narrative style with diagrams

User: Review this payment processing code

Claude: From a business analyst perspective:

Business Logic Analysis:
✓ Meets requirement: Process payment securely
✓ Implements acceptance criteria: Fraud detection
✓ Satisfies business rule: Minimum amount validation

Concerns:
• Missing user story link in comments
• Business logic for refunds not documented
• Need acceptance criteria for edge cases

Recommendation: Add user story references and document
the refund business process before proceeding.
```

### Software Engineer View

```
User: Load payment_gateway context with software_engineer persona

Claude: ✓ Loaded payment_gateway (PCI compliant)
        ✓ Applied software_engineer persona

Context Understanding:
• Focus: Code quality, unit tests, implementation
• View: Full technical details
• Testing: 90% unit coverage, 80% integration

User: Review this payment processing code

Claude: From a software engineer perspective:

Code Quality Analysis:
✓ Clean code principles followed
✓ SOLID principles applied
✓ Proper error handling
⚠ Missing unit tests for edge cases

Technical Issues:
• Function too long (65 lines, max 50)
• Cyclomatic complexity: 12 (max 10)
• Missing type hints on return value

Unit Test Coverage:
• Current: 75% (target: 90%)
• Missing tests: refund scenarios, timeout handling

Recommendation: Refactor into smaller functions, add type
hints, and increase unit test coverage to 90%.
```

### QA Engineer View

```
User: Load payment_gateway context with qa_engineer persona

Claude: ✓ Loaded payment_gateway (PCI compliant)
        ✓ Applied qa_engineer persona

Context Understanding:
• Focus: Test coverage, test automation, quality gates
• View: Test scenarios and edge cases
• Quality: Zero critical bugs required

User: Review this payment processing code

Claude: From a QA engineer perspective:

Test Coverage Analysis:
✓ Happy path covered
✓ Basic error scenarios tested
⚠ Edge cases missing

Missing Test Scenarios:
• Concurrent payment attempts
• Network timeout during processing
• Partial refund scenarios
• Maximum transaction amount
• Expired card scenarios

Test Data Concerns:
• Need test data for international cards
• Missing test data for various merchant types

Recommendation: Create comprehensive test plan covering
all edge cases, add automated tests for regression suite,
ensure 80% automation coverage.
```

---

## Benefits of Persona-Based Context

### For Team Members
✅ **Relevant Information**: See what matters for their role
✅ **Appropriate Detail Level**: Technical or business as needed
✅ **Role-Specific Checklists**: Focus on their responsibilities
✅ **Customized Views**: Filter out irrelevant information

### For Organizations
✅ **Role Clarity**: Clear responsibilities per persona
✅ **Consistent Standards**: Each role has defined standards
✅ **Better Collaboration**: Personas can work together
✅ **Audit Trail**: Track who reviewed what aspect

### For Claude
✅ **Role-Aware Responses**: Answer from perspective of role
✅ **Appropriate Recommendations**: Match persona expertise
✅ **Focus on Priorities**: Emphasize what matters for role
✅ **Multi-Perspective Analysis**: Review from multiple angles

---

## Implementation Strategy

### Phase 1: Core Personas
1. Create persona YAML files for 6-8 common roles
2. Add persona loading to ContextManager
3. Implement persona merging (highest priority)
4. Add switch_persona tool

### Phase 2: Persona Templates
1. Create documentation templates per persona
2. Add code review checklists per persona
3. Define notification preferences
4. Create persona-specific prompts

### Phase 3: Multi-Persona Support
1. Enable multiple personas simultaneously
2. Add persona comparison tools
3. Implement persona stacking
4. Create collaboration workflows

---

## Summary

**Personas add a crucial role-based layer** to the context management system:

🎭 **What**: Role-specific configuration overrides and preferences
📊 **Where**: Layer 5 (highest priority after runtime)
🎯 **Why**: Different roles need different views of the same project
🔄 **How**: YAML configs that merge with project context

**This enables**:
- Business analyst sees requirements and business logic
- Engineer sees code and technical details
- QA sees test coverage and quality gates
- DevOps sees deployment and infrastructure
- Security sees threats and compliance

**Claude can now act as ANY role on the team!** 🎭🧠
