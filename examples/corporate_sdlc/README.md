# Corporate SDLC Multi-Layer Configuration

A comprehensive example of using **AI_SDLC_config** for enterprise software development with multi-layered configuration management.

## Overview

This example demonstrates how a **corporate developer** can manage complex SDLC configurations across:
- **Corporate-wide policies** (security, compliance, standards)
- **Methodology layers** (Python, JavaScript, Java standards)
- **Project-specific requirements** (payment service, internal tools)
- **Runtime environments** (dev, staging, production)

## Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Runtime (Highest Priority)                        │
│   - Environment (dev/staging/prod)                          │
│   - User preferences                                        │
│   - Dynamic overrides                                       │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Project-Specific                                  │
│   - projects/payment_service.yml                            │
│   - projects/internal_dashboard.yml                         │
│   - Project docs, team, tools                              │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Methodology                                        │
│   - methodology/python_standards.yml                        │
│   - methodology/javascript_standards.yml                    │
│   - Language-specific standards                            │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Corporate Base (Lowest Priority)                  │
│   - corporate/base.yml                                      │
│   - Policies, compliance, security                         │
└─────────────────────────────────────────────────────────────┘
```

**Merge Priority**: Layer 4 > Layer 3 > Layer 2 > Layer 1

## Directory Structure

```
corporate_sdlc/
├── configs/
│   ├── corporate/
│   │   └── base.yml                    # Corporate policies (Layer 1)
│   ├── methodology/
│   │   ├── python_standards.yml        # Python standards (Layer 2)
│   │   └── javascript_standards.yml    # JS/TS standards (Layer 2)
│   └── projects/
│       ├── payment_service.yml         # Payment service (Layer 3)
│       └── internal_dashboard.yml      # Internal tool (Layer 3)
│
├── docs/
│   ├── policies/                       # Referenced by configs
│   │   ├── security_policy.md
│   │   ├── code_review_policy.md
│   │   ├── data_privacy_policy.md
│   │   └── incident_response.md
│   ├── methodologies/
│   │   ├── corporate_sdlc.md
│   │   ├── requirements_process.md
│   │   ├── design_process.md
│   │   ├── coding_standards.md
│   │   ├── python_coding_standards.md
│   │   ├── javascript_coding_standards.md
│   │   ├── testing_standards.md
│   │   └── deployment_process.md
│   └── projects/
│       ├── payment_service/
│       │   ├── architecture.md
│       │   ├── api_spec.yml
│       │   ├── runbook.md
│       │   └── pci_requirements.md
│       └── internal_dashboard/
│           ├── architecture.md
│           ├── components.md
│           └── style_guide.md
│
├── corporate_sdlc_demo.py             # Demo script
└── README.md                           # This file
```

## Layer Definitions

### Layer 1: Corporate Base
**File**: `configs/corporate/base.yml`

**Contains**:
- Organization metadata
- Corporate policies (security, privacy, code review, incident response)
- Compliance requirements (SOC2, ISO 27001, GDPR)
- SDLC methodology (requirements, design, coding, testing, deployment)
- Quality gates (code quality, security, performance)
- Tooling standards (git, CI/CD, monitoring, security tools)
- Documentation requirements
- Git standards (commit format, branch naming, protected branches)
- Security requirements (authentication, encryption, secrets management)
- Audit logging and compliance

**Applies to**: ALL projects

### Layer 2: Methodology
**Files**: `configs/methodology/{language}_standards.yml`

**Contains**:
- Language-specific coding standards
- Linting and formatting tools
- Testing frameworks and plugins
- Package management
- Security scanning tools specific to language

**Examples**:
- **Python**: PEP 8, pylint, pytest, poetry
- **JavaScript**: Airbnb style, eslint, jest, npm

**Applies to**: Projects using that language/framework

### Layer 3: Project-Specific
**Files**: `configs/projects/{project_name}.yml`

**Contains**:
- Project metadata (name, team, repo, classification)
- Project-specific documentation
- Overrides for coding standards (stricter or relaxed)
- Overrides for testing requirements
- Overrides for security requirements
- Overrides for quality gates
- Overrides for deployment approval chain
- Project-specific tools and services
- Team information
- Compliance requirements specific to project

**Examples**:
- **Payment Service**: Stricter (PCI compliance, 95% coverage, 4hr critical fix SLA)
- **Internal Dashboard**: Relaxed (75% coverage, simpler approval chain)

### Layer 4: Runtime
**Applied programmatically**

**Contains**:
- Environment (development, staging, production)
- User information (email, workstation)
- Dynamic overrides based on context
- Feature flags
- Temporary overrides

## Running the Demo

### Basic Usage

```bash
cd examples/corporate_sdlc

# View Payment Service configuration
python corporate_sdlc_demo.py payment_service

# View Internal Dashboard configuration
python corporate_sdlc_demo.py internal_dashboard

# Specify environment
python corporate_sdlc_demo.py payment_service production
```

### What You'll See

The demo displays:
1. **Configuration Loading** - Shows each layer being loaded
2. **Project Information** - Name, team, classification, PCI compliance
3. **Corporate Policies** - Security, code review, privacy, incident response
4. **Coding Standards** - Style guide, max lines, complexity, naming conventions
5. **Testing Requirements** - Min coverage, test types, frameworks
6. **Quality Gates** - Code quality thresholds, security scans
7. **Security Requirements** - Scan frequency, fix SLAs
8. **Deployment Approval Chain** - Who must approve each environment
9. **Compliance Frameworks** - SOC2, ISO 27001, GDPR, PCI DSS
10. **Project Documentation** - Architecture, API specs, runbooks
11. **Tools & Frameworks** - Language, package manager, testing tools
12. **Comparison** - Side-by-side comparison of projects

## Key Concepts

### 1. Policy Inheritance
All projects inherit corporate policies:
```yaml
# corporate/base.yml - Applies to ALL
corporate:
  policies:
    security:
      uri: "file://docs/policies/security_policy.md"
      mandatory: true
```

### 2. Methodology Customization
Language-specific standards override corporate:
```yaml
# methodology/python_standards.yml
methodology:
  coding:
    standards:
      style_guide: "PEP 8"  # Overrides corporate "corporate"
```

### 3. Project-Specific Requirements
Critical projects have stricter requirements:
```yaml
# projects/payment_service.yml
methodology:
  testing:
    min_coverage: 95  # Stricter than corporate 80%

security:
  vulnerability_management:
    critical_fix_sla_hours: 4  # Stricter than corporate 24hr
```

### 4. Runtime Flexibility
Environment-specific behavior:
```python
if environment == "production":
    overrides["security.scan_frequency"] = "continuous"
```

## Real-World Scenarios

### Scenario 1: New Python Microservice

```python
from ai_sdlc_config import ConfigManager

# Load layers
manager = ConfigManager()
manager.load_hierarchy("configs/corporate/base.yml")          # Layer 1
manager.load_hierarchy("configs/methodology/python_standards.yml")  # Layer 2
manager.load_hierarchy("configs/projects/new_microservice.yml")     # Layer 3
manager.add_runtime_overrides({"environment": "development"})       # Layer 4
manager.merge()

# Access configuration
min_coverage = manager.get_value("methodology.testing.min_coverage")
security_policy = manager.get_content("corporate.policies.security.uri")
```

### Scenario 2: Different Requirements by Criticality

**High-Security Project** (Payment Service):
- Min coverage: 95%
- Max code smells: 0
- Critical fix SLA: 4 hours
- Additional compliance: PCI DSS
- Deployment approval: Tech Lead + QA + Security + Compliance + CTO

**Internal Tool** (Dashboard):
- Min coverage: 75%
- Max code smells: 10
- Critical fix SLA: 24 hours (corporate default)
- Standard compliance: SOC2, ISO 27001
- Deployment approval: Tech Lead + Manager

### Scenario 3: Cross-Project Policy Updates

Update security policy once, applies everywhere:
```bash
# Edit docs/policies/security_policy.md
vim docs/policies/security_policy.md

# All projects automatically reference new version
# No config changes needed!
```

## Benefits of This Approach

### For Corporate Governance
✅ **Centralized policies** - One place to define corporate standards
✅ **Mandatory compliance** - Policies marked as mandatory
✅ **Audit trail** - All configs versioned in git
✅ **Consistency** - Same base for all projects

### For Development Teams
✅ **Clear requirements** - Know exactly what's expected
✅ **Language flexibility** - Python, JavaScript, Java standards
✅ **Project autonomy** - Override where justified
✅ **Easy onboarding** - New developers see full requirements

### For Security & Compliance
✅ **Security by default** - All projects get security policies
✅ **Risk-based approach** - Critical systems have stricter requirements
✅ **Traceable** - Know which policies apply to which projects
✅ **Auditable** - Configuration history in version control

### For Maintainability
✅ **URI-based docs** - Documentation lives separately
✅ **Single source of truth** - Update policy once
✅ **Version control** - Track changes over time
✅ **Scalable** - Add new projects easily

## Comparison: Payment Service vs Internal Dashboard

| Aspect | Payment Service | Internal Dashboard |
|--------|----------------|-------------------|
| **Classification** | Restricted | Internal |
| **PCI Compliant** | Yes | No |
| **Min Coverage** | 95% | 75% |
| **Max Code Smells** | 0 | 10 |
| **Critical Fix SLA** | 4 hours | 24 hours |
| **Security Scans** | Continuous | Daily |
| **Deployment Approval** | 5 people | 2 people |
| **Additional Compliance** | PCI DSS | None |
| **Test Types** | 6 types | 3 types |

**Both inherit**:
- Corporate policies (security, code review, privacy)
- Corporate tools (git, Jenkins, monitoring)
- Compliance frameworks (SOC2, ISO 27001, GDPR)
- Documentation requirements
- Git standards

## Extending the Example

### Add a New Project

1. Create project config:
```yaml
# configs/projects/new_project.yml
project:
  name: "New Project"
  team: "New Team"

# Override as needed
methodology:
  testing:
    min_coverage: 85
```

2. Create project docs:
```bash
mkdir docs/projects/new_project
vim docs/projects/new_project/architecture.md
```

3. Load in code:
```python
manager.load_hierarchy("configs/corporate/base.yml")
manager.load_hierarchy("configs/methodology/python_standards.yml")
manager.load_hierarchy("configs/projects/new_project.yml")
```

### Add a New Methodology

```yaml
# configs/methodology/java_standards.yml
methodology:
  coding:
    standards:
      style_guide: "Google Java Style"
      naming_convention: "camelCase"

  testing:
    framework: "JUnit 5"
```

### Add a New Policy

1. Create policy document:
```bash
vim docs/policies/api_design_policy.md
```

2. Reference in corporate base:
```yaml
# configs/corporate/base.yml
corporate:
  policies:
    api_design:
      uri: "file://docs/policies/api_design_policy.md"
      version: "1.0"
      mandatory: true
```

## Best Practices

1. **Keep corporate base stable** - Changes affect all projects
2. **Document overrides** - Explain why project overrides corporate
3. **Version policies** - Track policy changes over time
4. **Use URIs for documentation** - Keep configs small
5. **Test configuration** - Validate configs load correctly
6. **Review changes** - Corporate config changes need approval
7. **Communicate updates** - Alert teams when policies change
8. **Audit regularly** - Ensure compliance with policies

## Integration with CI/CD

```python
# In CI/CD pipeline
from ai_sdlc_config import ConfigManager

# Load project config
config = load_project_config(project_name, environment)

# Enforce quality gates
min_coverage = config.get_value("quality.gates.code_quality.min_test_coverage")
if actual_coverage < min_coverage:
    raise Exception(f"Coverage {actual_coverage}% < required {min_coverage}%")

# Verify security scans
if config.get_value("security.dependency_scan"):
    run_dependency_scan()

# Check approvals
approvers = config.get_value(f"methodology.deployment.approval_chain.{environment}")
verify_approvals(approvers)
```

## Conclusion

This example demonstrates how **AI_SDLC_config** enables:
- **Scalable governance** across many projects
- **Flexible requirements** based on project criticality
- **Language-specific** standards
- **Clear inheritance** with override capability
- **Documentation** as first-class configuration

Perfect for enterprise environments with multiple teams, languages, and compliance requirements.

---

*For questions or issues, see the main AI_SDLC_config repository.*
