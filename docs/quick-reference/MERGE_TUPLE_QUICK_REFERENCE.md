# Merge Tuple Quick Reference

## Your Merge Tuple Setup

```
ai_init_methodology  →  python_standards  →  payment_gateway
    (baseline)          (Python-specific)    (project-specific)
    Priority 0          Priority 1           Priority 2
```

---

## The Files

### 1. ai_init_methodology/project.json
```json
{
  "name": "ai_init_methodology",
  "base_projects": []                    // ← No dependencies (foundation)
}
```

### 2. python_standards/project.json
```json
{
  "name": "python_standards",
  "base_projects": [
    "ai_init_methodology"                // ← Inherits from methodology
  ]
}
```

### 3. payment_gateway/project.json
```json
{
  "name": "payment_gateway",
  "base_projects": [
    "ai_init_methodology",               // ← Foundation
    "python_standards"                   // ← Python standards
  ]
}
```

---

## What Happens When You Load payment_gateway

```python
/load-context payment_gateway
```

**System automatically:**

1. **Resolves dependencies**
   ```
   payment_gateway → needs [ai_init_methodology, python_standards]
   python_standards → needs [ai_init_methodology]
   ai_init_methodology → needs []
   ```

2. **Builds merge order** (topological sort)
   ```
   [ai_init_methodology, python_standards, payment_gateway]
   ```

3. **Loads configs**
   ```
   Layer 0: ai_init_methodology/config/config.yml
   Layer 1: python_standards/config/config.yml
   Layer 2: payment_gateway/config/config.yml
   ```

4. **Merges left to right** (later wins)
   ```
   result = merge([
       ai_init_methodology,    // Priority 0
       python_standards,       // Priority 1
       payment_gateway         // Priority 2 (wins conflicts)
   ])
   ```

---

## Example Merge

### Layer 0: ai_init_methodology
```yaml
methodology:
  quality_standards:
    testing:
      coverage_minimum: 80
```

### Layer 1: python_standards
```yaml
methodology:
  coding:
    style_guide: "PEP 8"
  quality_standards:
    testing:
      coverage_minimum: 85    # ← Overrides 80
```

### Layer 2: payment_gateway
```yaml
methodology:
  quality_standards:
    testing:
      coverage_minimum: 95    # ← Overrides 85
  coding:
    max_complexity: 7
```

### Final Result
```yaml
methodology:
  quality_standards:
    testing:
      coverage_minimum: 95    # ✅ From payment_gateway (highest priority)
  coding:
    style_guide: "PEP 8"      # ✅ From python_standards
    max_complexity: 7         # ✅ From payment_gateway
```

---

## Key Points

### 1. Array Order = Merge Priority
```json
"base_projects": [
  "ai_init_methodology",    // ← Merges first (lower priority)
  "python_standards"        // ← Merges second (higher priority)
]
// Current project merges last (highest priority)
```

### 2. Later Wins
```
Value from payment_gateway > Value from python_standards > Value from ai_init_methodology
```

### 3. Transitive Dependencies Resolved
```
You specify: payment_gateway → python_standards
System knows: python_standards → ai_init_methodology
Result: ai_init_methodology → python_standards → payment_gateway
```

### 4. Explicit is Better
```json
// Good: Be explicit about all dependencies
"base_projects": [
  "ai_init_methodology",     // Even though transitive
  "python_standards"
]

// Works but less clear
"base_projects": [
  "python_standards"         // ai_init_methodology is transitive
]
```

---

## Verify Your Tuple

```bash
# Load the context
/load-context payment_gateway

# See the full merge stack
/show-full-context
```

**Look for:**
```
## Configuration Layer Stack

**Merge Order**: ai_init_methodology → python_standards → payment_gateway

### Layer 0: ai_init_methodology
...

### Layer 1: python_standards
...

### Layer 2: payment_gateway
...
```

---

## Common Patterns

### Linear Chain (Your Pattern)
```
A → B → C
```
```json
A: {"base_projects": []}
B: {"base_projects": ["A"]}
C: {"base_projects": ["A", "B"]}
```

### Multiple Foundations
```
A ──┐
B ──┼──→ D
C ──┘
```
```json
D: {"base_projects": ["A", "B", "C"]}
```

### Shared Foundation
```
    A
   / \
  B   C
```
```json
A: {"base_projects": []}
B: {"base_projects": ["A"]}
C: {"base_projects": ["A"]}
```

---

## Quick Commands

```bash
# List all projects
/list-projects

# Load your tuple
/load-context payment_gateway

# See what got merged
/show-full-context

# Check a specific value
# (via MCP tool or ConfigManager)
manager.get_value("methodology.quality_standards.testing.coverage_minimum")
# Returns: 95
```

---

## Your Tuple is Ready! 🎯

```
ai_init_methodology (Sacred Seven + TDD)
    ↓
python_standards (PEP 8 + pytest)
    ↓
payment_gateway (95% coverage + PCI compliance)
```

**Merge priority**: Left to right (baseline → python → payment)

---

*Full guide: [CREATING_MERGE_TUPLES.md](CREATING_MERGE_TUPLES.md)*
