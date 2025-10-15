# Project Merge Keys Explained

## Question: What keys are the project merges done on?

**Short Answer**: Merges are done on **dot-notation path keys** (e.g., `methodology.testing.min_coverage`), and the merge algorithm recursively walks the YAML hierarchy, merging children at each level.

---

## How Merging Works

### 1. **Path-Based Merging**

Merges happen on the **hierarchical path** through the YAML structure:

```yaml
# Path: "methodology.testing.min_coverage"
methodology:
  testing:
    min_coverage: 80
```

### 2. **Child Key Matching**

At each level, children are matched by their **key name**:

```python
# From hierarchy_merger.py:143-150
for key, override_child in override.children.items():
    if key in result.children:
        # ✅ Child exists in both - merge recursively
        result.children[key] = self._merge_two_nodes(
            base=result.children[key],
            override=override_child,
            priority=priority
        )
```

### 3. **Recursive Deep Merge**

The algorithm merges **recursively** down the tree:
- Matches keys at current level
- Recurses into matching children
- Later values override earlier values

---

## Example: Payment Service Merge

### Layer 1: Corporate Base
```yaml
methodology:
  testing:
    min_coverage: 80        # Corporate default
    required_types:
      - "unit"
      - "integration"
      - "security"
```

### Layer 2: Python Methodology
```yaml
methodology:
  testing:
    min_coverage: 85        # Override: 80 → 85
    framework: "pytest"     # Add new key
```

### Layer 3: Payment Service Project
```yaml
methodology:
  testing:
    min_coverage: 95        # Override: 85 → 95
    required_types:
      - "unit"
      - "integration"
      - "security"
      - "penetration"       # Add to list
      - "load"              # Add to list
```

### Merged Result
```yaml
methodology:
  testing:
    min_coverage: 95        # ✅ Layer 3 wins (highest priority)
    framework: "pytest"     # ✅ From Layer 2 (only source)
    required_types:         # ✅ Layer 3 wins (complete override)
      - "unit"
      - "integration"
      - "security"
      - "penetration"
      - "load"
```

---

## Key Matching Algorithm

### Path Construction

Keys are matched at each level of the tree:

```
Root
├── methodology                    ← Match on "methodology"
│   ├── testing                   ← Match on "testing"
│   │   ├── min_coverage         ← Match on "min_coverage"
│   │   ├── framework            ← Match on "framework"
│   │   └── required_types       ← Match on "required_types"
│   ├── coding                    ← Match on "coding"
│   └── deployment                ← Match on "deployment"
├── security                       ← Match on "security"
└── quality                        ← Match on "quality"
```

### Full Path Examples

| Full Dot-Notation Path | Description |
|------------------------|-------------|
| `methodology.testing.min_coverage` | Test coverage requirement |
| `methodology.coding.standards.style_guide` | Code style guide |
| `security.vulnerability_management.critical_fix_sla_hours` | Security SLA |
| `quality.gates.code_quality.max_code_smells` | Quality gate |
| `corporate.policies.security.uri` | URI reference |

---

## Merge Strategy

### Default: OVERRIDE Strategy

From `hierarchy_merger.py:42`:
```python
def __init__(self, strategy: MergeStrategy = MergeStrategy.OVERRIDE):
    self.strategy = strategy
```

**OVERRIDE means**: Later layers completely replace earlier values.

### Merge Priority Order

```python
# From hierarchy_merger.py:54
hierarchies: List[HierarchyNode]  # Ordered by priority
                                   # (first = lowest, last = highest)

# Example:
merged = merger.merge([
    corporate_base,      # Priority 0 (lowest)
    python_methodology,  # Priority 1
    payment_project      # Priority 2 (highest - wins)
])
```

---

## Real-World Merge Example

### Setup
```python
# Layer 0: Corporate Base (01_corporate_base.yml)
methodology:
  testing:
    min_coverage: 80
  coding:
    standards:
      max_function_lines: 50
      max_complexity: 10
security:
  vulnerability_management:
    critical_fix_sla_hours: 24

# Layer 1: Python Methodology (02_methodology_python.yml)
methodology:
  testing:
    min_coverage: 85           # Override 80 → 85
    framework: "pytest"        # Add new key
  coding:
    linting:
      tools: ["pylint", "black"]  # Add new section

# Layer 2: Payment Service (03_project_payment_service.yml)
methodology:
  testing:
    min_coverage: 95           # Override 85 → 95
  coding:
    standards:
      max_function_lines: 30   # Override 50 → 30
      max_complexity: 7        # Override 10 → 7
security:
  vulnerability_management:
    critical_fix_sla_hours: 4  # Override 24 → 4
```

### Merge Process

#### Step 1: Match Top-Level Keys
```
Keys found across all layers:
- methodology  ✅ (in all 3 layers)
- security     ✅ (in Layer 0 and Layer 2)
```

#### Step 2: Recurse into "methodology"
```
methodology:
  - testing    ✅ (in all 3 layers) → Merge recursively
  - coding     ✅ (in all 3 layers) → Merge recursively
```

#### Step 3: Recurse into "methodology.testing"
```
methodology.testing:
  - min_coverage     ✅ Match on all 3:
      Layer 0: 80
      Layer 1: 85
      Layer 2: 95  ← Wins (highest priority)

  - framework        ✅ Match on Layer 1 only:
      Layer 1: "pytest"  ← Wins (only source)

  - required_types   ✅ Match on Layer 0 and Layer 2:
      Layer 0: ["unit", "integration", "security"]
      Layer 2: ["unit", "integration", "security", "penetration", "load"]
      Layer 2 wins (highest priority)
```

#### Step 4: Final Merged Result
```yaml
methodology:
  testing:
    min_coverage: 95               # Layer 2 (payment_service)
    framework: "pytest"            # Layer 1 (python_methodology)
    required_types:                # Layer 2 (payment_service)
      - "unit"
      - "integration"
      - "security"
      - "penetration"
      - "load"

  coding:
    standards:
      max_function_lines: 30       # Layer 2 (payment_service)
      max_complexity: 7            # Layer 2 (payment_service)
    linting:
      tools:                       # Layer 1 (python_methodology)
        - "pylint"
        - "black"

security:
  vulnerability_management:
    critical_fix_sla_hours: 4      # Layer 2 (payment_service)
```

---

## Key Matching Rules

### Rule 1: Exact Key Match
Keys must match **exactly** at each level:

```yaml
# ✅ Matches
base:
  methodology:
    testing: ...

override:
  methodology:     # ✅ "methodology" matches
    testing: ...   # ✅ "testing" matches

# ❌ Does NOT match
base:
  methodology:
    testing: ...

override:
  methodologies:   # ❌ "methodologies" ≠ "methodology"
    testing: ...
```

### Rule 2: Case-Sensitive
```yaml
# ❌ Does NOT match
base:
  Security: ...

override:
  security: ...   # ❌ "security" ≠ "Security"
```

### Rule 3: Type Matters
```yaml
# Value node (leaf) vs Container node (has children)

base:
  min_coverage: 80              # Leaf node (value)

override:
  min_coverage:                 # Container node (children)
    unit: 90
    integration: 80
# Result depends on MergeStrategy:
# - OVERRIDE: override wins, base value lost
# - PRESERVE: base wins, override ignored
```

---

## Special Cases

### 1. URI References

URI references are treated as **opaque values**:

```yaml
base:
  principles:
    _uri: "file://docs/base_principles.md"

override:
  principles:
    _uri: "file://docs/override_principles.md"

# Result:
principles:
  _uri: "file://docs/override_principles.md"  # Override wins
```

### 2. Lists/Arrays

Lists are **replaced entirely**, not merged:

```yaml
base:
  required_types: ["unit", "integration"]

override:
  required_types: ["unit", "security"]

# Result:
required_types: ["unit", "security"]  # ❌ NOT merged, completely replaced
```

### 3. New Keys

Keys that exist in only one layer are added:

```yaml
base:
  testing:
    min_coverage: 80

override:
  testing:
    framework: "pytest"     # New key

# Result:
testing:
  min_coverage: 80          # From base
  framework: "pytest"       # Added from override
```

### 4. Removed Keys

**Cannot remove keys** - can only override with different values:

```yaml
base:
  testing:
    min_coverage: 80
    framework: "unittest"

override:
  testing:
    min_coverage: 90
    # ⚠️ Cannot remove "framework" - it remains

# Result:
testing:
  min_coverage: 90          # Overridden
  framework: "unittest"     # Still present (from base)
```

---

## Merge Key Categories

### 1. Top-Level Organizational Keys
```yaml
organization:        # Company info
corporate:          # Corporate policies
methodology:        # Development process
quality:            # Quality standards
security:           # Security requirements
compliance:         # Compliance frameworks
tools:              # Tooling
documentation:      # Documentation requirements
git:                # Git standards
team:               # Team information
project:            # Project metadata
```

### 2. Common Merge Paths

| Path | Description | Typical Override Pattern |
|------|-------------|-------------------------|
| `methodology.testing.min_coverage` | Test coverage % | 80 → 85 → 95 (stricter) |
| `methodology.coding.standards.max_complexity` | Cyclomatic complexity | 10 → 7 → 5 (stricter) |
| `security.vulnerability_management.critical_fix_sla_hours` | Fix SLA | 24 → 4 (faster) |
| `quality.gates.code_quality.max_code_smells` | Code smells | 5 → 0 (stricter) |
| `methodology.deployment.approval_chain` | Approvers | Add more approvers |

---

## How ConfigManager Uses Merge Keys

### Access via Dot Notation

```python
from ai_sdlc_config import ConfigManager

# Create manager and load hierarchies
manager = ConfigManager()
manager.load_hierarchy("01_corporate_base.yml")
manager.load_hierarchy("02_methodology_python.yml")
manager.load_hierarchy("03_project_payment_service.yml")

# Merge all layers
manager.merge()

# Access merged values via dot notation
coverage = manager.get_value("methodology.testing.min_coverage")
# Returns: 95 (from highest priority layer)

style = manager.get_value("methodology.coding.standards.style_guide")
# Returns: "PEP 8" (from python methodology layer)

sla = manager.get_value("security.vulnerability_management.critical_fix_sla_hours")
# Returns: 4 (from payment service layer)
```

### Wildcard Searches

```python
# Find all testing-related configs
testing_configs = manager.find_all("methodology.testing.*")
# Returns: All keys under methodology.testing

# Find all security configs
security_configs = manager.find_all("security.*")
```

---

## Summary

### Merge Keys Are:
1. **Path-based**: Dot-notation paths through YAML hierarchy
2. **Exact match**: Keys must match exactly at each level
3. **Recursive**: Merging happens recursively down the tree
4. **Priority-based**: Later layers override earlier layers
5. **Type-aware**: Leaf nodes vs container nodes matter

### Merge Algorithm:
```
For each level in hierarchy:
  1. Match child keys by name
  2. If key exists in both:
     - Recurse into children
     - Apply merge strategy (OVERRIDE by default)
  3. If key exists in only one:
     - Add to result
  4. Continue to next level
```

### Common Merge Pattern:
```
Corporate Base (broad defaults)
    ↓ (more specific)
Methodology Layer (language/framework standards)
    ↓ (more specific)
Project Layer (strict project requirements)
    ↓ (most specific)
Persona Layer (role-based view)
```

---

## Questions?

**Q: Can I merge on different keys?**
A: Yes, any YAML key can be a merge point. The algorithm works on the structure.

**Q: Can I append to arrays instead of replacing?**
A: Not by default. Arrays are replaced entirely. You'd need a custom merge strategy.

**Q: Can I remove keys from base layers?**
A: No, you can only override values. Keys from base layers persist unless explicitly overridden.

**Q: Are merges case-sensitive?**
A: Yes, "Security" ≠ "security".

**Q: Can I merge across different root keys?**
A: Yes, each top-level key is merged independently.

---

*For implementation details, see: `src/ai_sdlc_config/mergers/hierarchy_merger.py`*
