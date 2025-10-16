# Merge Keys - Quick Reference

## Question: What keys are the project merges done on?

**Answer**: Merges are done on **dot-notation path keys** through the YAML hierarchy.

---

## Visual Example

### Three Layers
```yaml
# Layer 0: Corporate Base
methodology:
  testing:
    min_coverage: 80
  coding:
    max_complexity: 10

# Layer 1: Python Methodology
methodology:
  testing:
    min_coverage: 85      # ← Overrides 80
    framework: "pytest"    # ← New key
  coding:
    max_complexity: 10    # ← Unchanged

# Layer 2: Payment Service
methodology:
  testing:
    min_coverage: 95      # ← Overrides 85
  coding:
    max_complexity: 7     # ← Overrides 10
```

### Merged Result
```yaml
methodology:
  testing:
    min_coverage: 95         # ✅ Layer 2 (highest priority)
    framework: "pytest"      # ✅ Layer 1 (only source)
  coding:
    max_complexity: 7        # ✅ Layer 2 (highest priority)
```

---

## Key Matching

### How Keys Match

At each level, children match by **key name**:

```
methodology                    ← Match on "methodology"
    ├── testing               ← Match on "testing"
    │   ├── min_coverage     ← Match on "min_coverage"
    │   └── framework        ← Match on "framework"
    └── coding               ← Match on "coding"
        └── max_complexity   ← Match on "max_complexity"
```

### Dot-Notation Paths

| Path | Merge Point |
|------|-------------|
| `methodology.testing.min_coverage` | Test coverage |
| `methodology.coding.max_complexity` | Code complexity |
| `security.vulnerability_management.critical_fix_sla_hours` | Security SLA |
| `quality.gates.code_quality.max_code_smells` | Quality gate |

---

## Merge Rules

### Rule 1: Exact Key Match
```yaml
✅ "methodology" matches "methodology"
❌ "methodology" does NOT match "methodologies"
❌ "Security" does NOT match "security" (case-sensitive)
```

### Rule 2: Later Wins (OVERRIDE Strategy)
```yaml
Layer 0: min_coverage: 80
Layer 1: min_coverage: 85
Layer 2: min_coverage: 95

Result: 95  # ✅ Layer 2 wins (highest priority)
```

### Rule 3: New Keys Are Added
```yaml
Layer 0:
  testing:
    min_coverage: 80

Layer 1:
  testing:
    framework: "pytest"    # New key

Result:
  testing:
    min_coverage: 80       # From Layer 0
    framework: "pytest"    # From Layer 1
```

### Rule 4: Lists Replace (Not Merge)
```yaml
Layer 0: required_types: ["unit", "integration"]
Layer 1: required_types: ["unit", "security"]

Result: ["unit", "security"]  # ✅ Complete replacement
```

---

## Common Merge Patterns

### Pattern 1: Progressive Strictness
```
Corporate:   min_coverage: 80
Methodology: min_coverage: 85
Project:     min_coverage: 95

Result: 95 (strictest)
```

### Pattern 2: Adding Requirements
```
Corporate:   required_types: ["unit", "integration"]
Project:     required_types: ["unit", "integration", "security", "penetration"]

Result: ["unit", "integration", "security", "penetration"]
```

### Pattern 3: Faster SLAs
```
Corporate: critical_fix_sla_hours: 24
Project:   critical_fix_sla_hours: 4

Result: 4 (faster)
```

---

## Top-Level Merge Keys

Standard top-level keys used in configurations:

```yaml
organization:        # Company/division info
corporate:          # Corporate policies (URIs)
methodology:        # Development process
  requirements:     # Requirements process
  design:           # Design process
  coding:           # Coding standards
  testing:          # Testing standards
  deployment:       # Deployment process
quality:            # Quality gates
  gates:            # Quality thresholds
security:           # Security requirements
  authentication:   # Auth methods
  encryption:       # Encryption standards
  vulnerability_management:  # Vuln scanning
compliance:         # Compliance frameworks
  frameworks:       # (PCI, SOC2, etc.)
  audit_logging:    # Audit requirements
tools:              # Tooling configuration
  version_control:  # Git, etc.
  ci_cd:            # Jenkins, etc.
  monitoring:       # DataDog, etc.
documentation:      # Doc requirements
git:                # Git standards
  commit_message_format:
  branch_naming:
team:               # Team information
project:            # Project metadata
```

---

## Access Merged Values

### Via ConfigManager
```python
from ai_sdlc_config import ConfigManager

manager = ConfigManager()
manager.load_hierarchy("01_corporate_base.yml")
manager.load_hierarchy("02_methodology_python.yml")
manager.load_hierarchy("03_project_payment_service.yml")
manager.merge()

# Get merged value
coverage = manager.get_value("methodology.testing.min_coverage")
# Returns: 95
```

### Via ContextManager (MCP)
```python
from mcp_service.server.context_tools import ContextManager

context_mgr = ContextManager(repository=repo)
context = context_mgr.load_context("payment_service")

# Access merged configuration
coverage = context["requirements"]["testing"]["min_coverage"]
# Returns: 95
```

---

## Merge Priority Order

```
Priority 0 (Lowest):  Corporate Base
    ↓
Priority 1:           Methodology (Python/Java/JS)
    ↓
Priority 2:           Project-Specific
    ↓
Priority 3 (Highest): Persona Override (runtime)
```

**Rule**: Higher priority always wins.

---

## Key Insight

The merge system is **path-based** and **hierarchical**:

1. **Path-based**: Merges on dot-notation paths (`methodology.testing.min_coverage`)
2. **Hierarchical**: Walks the tree recursively, matching keys at each level
3. **Priority-based**: Later layers override earlier layers
4. **Additive**: New keys are added, existing keys are overridden

**It's NOT a flat key-value merge** - it's a **tree merge** that respects hierarchy.

---

*Full details: [MERGE_KEYS_EXPLAINED.md](MERGE_KEYS_EXPLAINED.md)*
