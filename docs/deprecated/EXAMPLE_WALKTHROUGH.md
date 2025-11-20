# ai_sdlc_method Example Walkthrough

## What You Just Saw

A complete working example of the MCP service managing configuration projects for an enterprise.

## Repository Structure Created

```
example_projects_repo/
├── .git/                                    # Git repository
├── projects.json                            # Project registry
├── acme_corporate/                          # Base project
│   ├── project.json
│   ├── config/config.yml
│   └── docs/
├── python_standards/                        # Methodology project
│   ├── project.json
│   ├── config/config.yml
│   └── docs/
├── payment_gateway/                         # Custom project (strict)
│   ├── project.json
│   ├── config/config.yml
│   └── docs/
│       └── architecture/
│           └── system_design.md
├── admin_dashboard/                         # Custom project (relaxed)
│   ├── project.json
│   ├── config/config.yml
│   └── docs/
└── merged_projects/
    └── payment_gateway_prod_v1_0_0/        # Merged project
        ├── project.json
        ├── .merge_info.json                # Merge provenance
        └── config/
            └── merged.yml                   # Full merged config
```

## Step-by-Step Breakdown

### 1. Corporate Base Project

```yaml
# acme_corporate/config/config.yml
corporate:
  name: Acme Corporation
  policies:
    security: {uri: "file://docs/policies/security_policy.md", mandatory: true}
    code_review: {uri: "file://docs/policies/code_review.md", mandatory: true}

methodology:
  testing:
    min_coverage: 80                    # Corporate default
  coding:
    max_function_lines: 50
    max_complexity: 10
```

**Purpose**: Company-wide policies that apply to ALL projects.

---

### 2. Python Methodology Project

```yaml
# python_standards/config/config.yml
methodology:
  coding:
    standards:
      style_guide: "PEP 8"
      formatter: "black"
    linting:
      tools: ["pylint", "flake8", "mypy", "black"]
  testing:
    framework: "pytest"
    plugins: ["pytest-cov", "pytest-mock", "pytest-asyncio"]
```

**Purpose**: Language-specific standards for Python projects.
**Inherits from**: `acme_corporate`

---

### 3. Payment Gateway (Custom Project - Strict)

```yaml
# payment_gateway/config/config.yml
project:
  name: Payment Gateway
  classification: restricted
  pci_compliant: true

methodology:
  testing:
    min_coverage: 95                    # STRICTER than corporate 80%
    required_types:
      - unit
      - integration
      - security
      - penetration                     # Additional test types
      - load

security:
  vulnerability_management:
    critical_fix_sla_hours: 4           # Strict SLA
```

**Purpose**: High-security payment processing with PCI compliance.
**Inherits from**: `acme_corporate` → `python_standards`
**Overrides**: Testing coverage (95% vs 80%), additional security requirements

---

### 4. Admin Dashboard (Custom Project - Relaxed)

```yaml
# admin_dashboard/config/config.yml
project:
  name: Admin Dashboard
  classification: internal

methodology:
  testing:
    min_coverage: 75                    # MORE RELAXED than corporate 80%

quality:
  gates:
    code_quality:
      max_code_smells: 30               # More lenient
```

**Purpose**: Internal operations dashboard with lower security requirements.
**Inherits from**: `acme_corporate` → `python_standards`
**Overrides**: Lower testing coverage (75% vs 80%), relaxed quality gates

---

### 5. Merged Project for Production

```yaml
# merged_projects/payment_gateway_prod_v1_0_0/config/merged.yml
# (FULL merged configuration - 100+ lines)

corporate:
  name: Acme Corporation
  policies: { ... }                     # From acme_corporate

methodology:
  testing:
    min_coverage: 95                    # From payment_gateway override
    framework: pytest                   # From python_standards
  coding:
    standards:
      style_guide: PEP 8                # From python_standards
    max_function_lines: 50              # From acme_corporate

project:
  name: Payment Gateway                 # From payment_gateway
  pci_compliant: true

environment: production                 # From runtime_overrides
build:
  version: 1.0.0                        # From runtime_overrides
  timestamp: 2025-10-14T16:00:00Z
deployment:
  replicas: 5                           # From runtime_overrides
  auto_scaling: true
```

**Merge Info** (`.merge_info.json`):
```json
{
  "source_projects": [
    "acme_corporate",
    "python_standards",
    "payment_gateway"
  ],
  "merge_date": "2025-10-14T16:11:15.672842Z",
  "runtime_overrides": {
    "environment": "production",
    "build": { "version": "1.0.0", ... },
    "deployment": { "replicas": 5, ... }
  }
}
```

**Purpose**: Immutable deployment snapshot with full configuration.
**Contains**: Complete merged config from all source projects + runtime overrides.
**Use case**: Production deployment, CI/CD pipeline.

---

## Key Differences: Custom vs Merged

| Aspect | Payment Gateway (Custom) | Payment Gateway Prod (Merged) |
|--------|-------------------------|-------------------------------|
| **Type** | `custom` | `merged` |
| **Config File** | `config/config.yml` | `config/merged.yml` |
| **Content** | Only explicit overrides (45 lines) | Full merged config (100+ lines) |
| **Metadata** | `base_projects: [...]` | `merged_from: [...]`, `merge_date`, `runtime_overrides` |
| **Mutability** | Living, can be updated | Immutable snapshot |
| **Use Case** | Active development | Deployment to production |
| **Git Commits** | "Update project: payment_gateway" | "Merge projects into payment_gateway_prod_v1_0_0: ..." |

---

## Configuration Inheritance Flow

```
┌─────────────────────────────────────────────────────────────┐
│ acme_corporate (base)                                       │
│   • min_coverage: 80                                        │
│   • max_function_lines: 50                                  │
│   • policies: security, code_review                         │
└────────────────┬────────────────────────────────────────────┘
                 │ inherits
┌────────────────▼────────────────────────────────────────────┐
│ python_standards (methodology)                              │
│   • style_guide: PEP 8                                      │
│   • linting: pylint, flake8, mypy                          │
│   • testing: pytest                                         │
│   (inherits all from acme_corporate)                        │
└────────────────┬────────────────────────────────────────────┘
                 │ inherits
┌────────────────▼────────────────────────────────────────────┐
│ payment_gateway (custom)                                    │
│   • min_coverage: 95  ← OVERRIDES corporate 80%            │
│   • pci_compliant: true  ← NEW                             │
│   • critical_fix_sla_hours: 4  ← NEW                       │
│   (inherits all from python_standards + acme_corporate)     │
└────────────────┬────────────────────────────────────────────┘
                 │ merge
┌────────────────▼────────────────────────────────────────────┐
│ payment_gateway_prod_v1_0_0 (merged)                       │
│   • environment: production  ← RUNTIME                     │
│   • build.version: 1.0.0  ← RUNTIME                        │
│   • deployment.replicas: 5  ← RUNTIME                      │
│   (contains FULL merged config from all sources)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Git Audit Trail

Every operation creates a git commit:

```bash
$ git log --oneline

c6ee6da Merge projects into payment_gateway_prod_v1_0_0: acme_corporate, python_standards, payment_gateway
d29f8b3 Create project: admin_dashboard
6cc3031 Update project: payment_gateway
bfb1693 Add document to payment_gateway: architecture/system_design.md
6ec928f Create project: payment_gateway
d8ebe00 Create project: python_standards
89157a7 Create project: acme_corporate
cb5e89f Initialize project repository
```

---

## Comparison: Payment Gateway vs Admin Dashboard

| Metric | Payment Gateway | Admin Dashboard |
|--------|----------------|----------------|
| Classification | `restricted` | `internal` |
| PCI Compliant | `true` | `false` |
| Min Coverage | **95%** (stricter) | **75%** (relaxed) |
| Max Code Smells | **0** (no tolerance) | **30** (lenient) |
| Security SLA | **4 hours** | 24 hours (default) |
| Test Types | 5 types (incl. penetration) | 2 types (unit, integration) |

**Why?**
- Payment Gateway: Financial data, PCI compliance, high security
- Admin Dashboard: Internal tool, lower risk

---

## Real-World Usage in CI/CD

```python
from mcp_service.storage.project_repository import ProjectRepository

# Load repository
repo = ProjectRepository("/path/to/projects_repo")

# Merge for deployment
merged = repo.merge_projects(
    source_projects=["acme_corporate", "python_standards", "payment_gateway"],
    target_name=f"payment_gateway_prod_v{version}",
    runtime_overrides={
        "environment": "production",
        "build": {
            "version": version,
            "commit": git_commit_sha,
            "timestamp": datetime.utcnow().isoformat()
        },
        "deployment": {
            "region": "us-east-1",
            "replicas": 5
        }
    }
)

# Validate configuration
config = repo.get_project_config(merged.name)

min_coverage = config.get_value("methodology.testing.min_coverage")
if actual_coverage < min_coverage:
    raise Exception(f"Coverage {actual_coverage}% < required {min_coverage}%")

# Deploy...
print(f"Deploying {merged.name} to production")
```

---

## Try It Yourself

```bash
# Run the example
cd /Users/jim/src/apps/ai_sdlc_method
python mcp_service/examples/quick_start_example.py

# Explore the repository
cd example_projects_repo
git log --oneline
cat projects.json
cat payment_gateway/config/config.yml
cat merged_projects/payment_gateway_prod_v1_0_0/config/merged.yml

# View merge metadata
cat merged_projects/payment_gateway_prod_v1_0_0/.merge_info.json
```

---

## Benefits Demonstrated

✅ **Inheritance**: Projects inherit from base + methodology layers
✅ **Overrides**: Each project can customize based on requirements
✅ **Merge**: Creates deployment-ready immutable snapshots
✅ **Runtime Overrides**: Environment-specific config at merge time
✅ **Git Audit**: Full history of all changes
✅ **Distinction**: Custom projects (living) vs Merged projects (immutable)
✅ **Flexibility**: Strict for payments, relaxed for internal tools
✅ **Documentation**: URIs to external docs, git-backed

---

## Next Steps

1. **Use with Claude Desktop**: Configure MCP server for natural language queries
2. **CI/CD Integration**: Use in deployment pipelines
3. **Add More Projects**: Create projects for different teams/services
4. **LLM Inspection**: Query projects using natural language
5. **Compare Projects**: Analyze differences in requirements

See `mcp_service/README.md` and `mcp_service/docs/API.md` for complete documentation.
