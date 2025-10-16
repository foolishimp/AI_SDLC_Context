# Creating Merge Tuples (Inheritance Chains)

## Your Question

> "How do I create my merge tuple where:
> 1. `ai_init_methodology` is my baseline
> 2. Then override with `python_standards`
> 3. Finally override with `payment_gateway`
>
> So priority is: left to right (baseline → python → payment)"

---

## Answer: Use `base_projects` Field

Create an **inheritance chain** by setting the `base_projects` field in each project's `project.json`.

### Your Desired Merge Order

```
ai_init_methodology  (Priority 0 - Baseline)
    ↓
python_standards     (Priority 1 - Adds Python-specific standards)
    ↓
payment_gateway      (Priority 2 - Adds payment-specific requirements)
```

---

## Step-by-Step Setup

### Step 1: ai_init_methodology (Baseline)

**File**: `ai_init_methodology/project.json`

```json
{
  "name": "ai_init_methodology",
  "project_type": "methodology",
  "version": "1.0.0",
  "base_projects": [],           // ← No dependencies (it's the foundation)
  "description": "Core development methodology: Sacred Seven principles and TDD workflow"
}
```

**Why**: This is your **foundation** - nothing below it.

---

### Step 2: python_standards (Inherits from ai_init_methodology)

**File**: `python_standards/project.json`

```json
{
  "name": "python_standards",
  "project_type": "methodology",
  "version": "1.0.0",
  "base_projects": [
    "ai_init_methodology"        // ← Inherits from methodology
  ],
  "description": "Python-specific coding standards and tools"
}
```

**Why**: Python standards **builds on** the Sacred Seven methodology.

---

### Step 3: payment_gateway (Inherits from python_standards)

**File**: `payment_gateway/project.json`

```json
{
  "name": "payment_gateway",
  "project_type": "project",
  "version": "1.0.0",
  "base_projects": [
    "ai_init_methodology",       // ← Foundation
    "python_standards"           // ← Python-specific standards
  ],
  "description": "High-security payment processing gateway with PCI compliance"
}
```

**Why**: Payment gateway inherits **both** methodology and Python standards.

---

## How the Merge Works

### When You Load "payment_gateway"

```python
# System automatically resolves the inheritance chain:
context_manager.load_context("payment_gateway")
```

**What happens internally:**

```
1. Resolve dependencies:
   payment_gateway → needs [ai_init_methodology, python_standards]
   python_standards → needs [ai_init_methodology]
   ai_init_methodology → needs []

2. Build ordered list (topological sort):
   [ai_init_methodology, python_standards, payment_gateway]

3. Load configs in order:
   - ai_init_methodology/config/config.yml       (Priority 0)
   - python_standards/config/config.yml          (Priority 1)
   - payment_gateway/config/config.yml           (Priority 2)

4. Merge from lowest to highest priority:
   result = merge([
       ai_init_methodology_config,    // Priority 0 (lowest)
       python_standards_config,        // Priority 1
       payment_gateway_config          // Priority 2 (highest - wins conflicts)
   ])
```

---

## Merge Priority Visualization

```
Layer 0: ai_init_methodology
├── methodology.principles (Sacred Seven)
├── methodology.processes (TDD workflow)
└── quality_standards (80% coverage, etc.)

     ↓ (merged into)

Layer 1: python_standards
├── methodology.coding.style_guide = "PEP 8"        ← Adds Python specifics
├── methodology.testing.framework = "pytest"        ← Adds Python framework
└── methodology.coding.linting.tools = ["pylint"]   ← Adds Python tools

     ↓ (merged into)

Layer 2: payment_gateway
├── methodology.testing.min_coverage = 95           ← Overrides to stricter
├── security.pci_compliance = true                  ← Adds payment requirements
└── methodology.coding.max_complexity = 7           ← Overrides to stricter

     ↓ (results in)

Final Materialized Context
├── methodology.principles (from Layer 0)
├── methodology.processes (from Layer 0)
├── methodology.coding.style_guide = "PEP 8" (from Layer 1)
├── methodology.testing.framework = "pytest" (from Layer 1)
├── methodology.testing.min_coverage = 95 (from Layer 2 - wins!)
├── security.pci_compliance = true (from Layer 2)
└── methodology.coding.max_complexity = 7 (from Layer 2 - wins!)
```

---

## Current vs Desired State

### Current State (What You Have Now)

```json
// ai_init_methodology/project.json
{
  "base_projects": []
}

// python_standards/project.json
{
  "base_projects": ["acme_corporate"]     // ← Currently inherits from acme_corporate
}

// payment_gateway/project.json
{
  "base_projects": [
    "acme_corporate",
    "python_standards"
  ]
}
```

**Current merge order**: `acme_corporate → python_standards → payment_gateway`

### Desired State (Your Request)

```json
// ai_init_methodology/project.json
{
  "base_projects": []                      // ✅ No change (foundation)
}

// python_standards/project.json
{
  "base_projects": ["ai_init_methodology"] // ← CHANGE: Inherit from methodology
}

// payment_gateway/project.json
{
  "base_projects": [
    "ai_init_methodology",                 // ← CHANGE: Explicit foundation
    "python_standards"                     // ← Keep this
  ]
}
```

**Desired merge order**: `ai_init_methodology → python_standards → payment_gateway`

---

## Making the Changes

### Option 1: Manual Edit (Quick)

**Edit `python_standards/project.json`:**
```json
{
  "name": "python_standards",
  "project_type": "methodology",
  "version": "1.0.0",
  "base_projects": [
    "ai_init_methodology"        // ← Changed from "acme_corporate"
  ],
  "description": "Python-specific coding standards and tools"
}
```

**Edit `payment_gateway/project.json`:**
```json
{
  "name": "payment_gateway",
  "project_type": "project",
  "version": "1.0.0",
  "base_projects": [
    "ai_init_methodology",       // ← Added explicitly
    "python_standards"            // ← Keep this
  ],
  "description": "High-security payment processing gateway with PCI compliance"
}
```

### Option 2: Using MCP Tools (Programmatic)

```python
from mcp_service.storage.project_repository import ProjectRepository
from pathlib import Path

repo = ProjectRepository(root_path=Path("example_projects_repo"))

# Update python_standards
python_std = repo.get_project("python_standards")
python_std.base_projects = ["ai_init_methodology"]
repo.save_project(python_std)

# Update payment_gateway
payment = repo.get_project("payment_gateway")
payment.base_projects = ["ai_init_methodology", "python_standards"]
repo.save_project(payment)
```

---

## Verification

### After Making Changes

```bash
# Load payment_gateway context
/load-context payment_gateway

# Show the full merged state
/show-full-context
```

**Expected output:**

```
================================================================================
🎯 FULL CONTEXT STATE: payment_gateway
================================================================================

## Configuration Layer Stack

**Merge Order**: ai_init_methodology → python_standards → payment_gateway

### Layer 0: ai_init_methodology
- **File**: `config.yml`
- **Description**: Sacred Seven methodology foundation
- **Path**: `.../ai_init_methodology/config/config.yml`

### Layer 1: python_standards
- **File**: `config.yml`
- **Description**: Python-specific standards
- **Path**: `.../python_standards/config/config.yml`

### Layer 2: payment_gateway
- **File**: `config.yml`
- **Description**: Payment-specific requirements
- **Path**: `.../payment_gateway/config/config.yml`

## Materialized Context (Merged Configuration)

### Methodology
- **Sacred Seven Principles**: ✅ (from ai_init_methodology)
- **TDD Workflow**: ✅ (from ai_init_methodology)
- **Style Guide**: PEP 8 (from python_standards)
- **Testing Framework**: pytest (from python_standards)
- **Min Coverage**: 95% (from payment_gateway - overridden!)

### Security
- **PCI Compliance**: true (from payment_gateway)
```

---

## Understanding base_projects Array

### Single Dependency

```json
{
  "base_projects": ["ai_init_methodology"]
}
```
**Meaning**: Inherit from one project only.

### Multiple Dependencies

```json
{
  "base_projects": [
    "ai_init_methodology",
    "python_standards"
  ]
}
```

**Meaning**: Inherit from **both** projects.

**Merge order**: Array order matters!
- `ai_init_methodology` merges first (lower priority)
- `python_standards` merges second (higher priority)
- Current project merges last (highest priority)

### Transitive Dependencies

```json
// python_standards depends on ai_init_methodology
{
  "name": "python_standards",
  "base_projects": ["ai_init_methodology"]
}

// payment_gateway depends on python_standards
{
  "name": "payment_gateway",
  "base_projects": ["python_standards"]
}
```

**System automatically resolves**:
```
payment_gateway needs python_standards
python_standards needs ai_init_methodology
ai_init_methodology needs nothing

Final order: [ai_init_methodology, python_standards, payment_gateway]
```

**Best practice**: Be explicit! List all direct dependencies:
```json
{
  "name": "payment_gateway",
  "base_projects": [
    "ai_init_methodology",    // ← Explicit (even though transitive)
    "python_standards"
  ]
}
```

---

## Common Patterns

### Pattern 1: Linear Chain (What You Want)

```
Foundation → Methodology → Project
```

```json
// Foundation
{"name": "ai_init_methodology", "base_projects": []}

// Methodology
{"name": "python_standards", "base_projects": ["ai_init_methodology"]}

// Project
{"name": "payment_gateway", "base_projects": ["ai_init_methodology", "python_standards"]}
```

### Pattern 2: Multiple Foundations

```
Foundation A ──┐
               ├──→ Project
Foundation B ──┘
```

```json
{
  "name": "my_project",
  "base_projects": [
    "security_baseline",
    "data_privacy_baseline"
  ]
}
```

### Pattern 3: Diamond Dependency (Handle Carefully)

```
      Base
      /  \
     A    B
      \  /
    Project
```

```json
// Base
{"name": "corporate_base", "base_projects": []}

// A
{"name": "python_standards", "base_projects": ["corporate_base"]}

// B
{"name": "security_baseline", "base_projects": ["corporate_base"]}

// Project (diamond)
{
  "name": "payment_gateway",
  "base_projects": [
    "corporate_base",      // ← Listed once
    "python_standards",
    "security_baseline"
  ]
}
```

**System handles**: Deduplicates `corporate_base` (merges only once).

---

## Complete Example with Configs

### ai_init_methodology/config/config.yml

```yaml
methodology:
  principles:
    _uri: "file://docs/principles/SACRED_SEVEN.md"
    test_driven_development:
      principle: 1
      mantra: "No code without tests"

  quality_standards:
    testing:
      coverage_minimum: 80
      coverage_target: 100
```

### python_standards/config/config.yml

```yaml
methodology:
  coding:
    style_guide: "PEP 8"
    linting:
      tools:
        - "pylint"
        - "black"
        - "mypy"

  testing:
    framework: "pytest"
    coverage_minimum: 85    # ← Overrides 80 from ai_init_methodology
```

### payment_gateway/config/config.yml

```yaml
project:
  name: "Payment Gateway"
  pci_compliant: true

methodology:
  testing:
    coverage_minimum: 95    # ← Overrides 85 from python_standards

  coding:
    max_complexity: 7       # ← Stricter for payments

security:
  pci_dss:
    level: "Level 1"
    requirements_uri: "file://docs/pci_requirements.md"
```

### Final Merged Result

```yaml
methodology:
  principles:                        # ✅ From ai_init_methodology
    _uri: "file://docs/principles/SACRED_SEVEN.md"
    test_driven_development:
      principle: 1
      mantra: "No code without tests"

  quality_standards:                 # ✅ From ai_init_methodology
    testing:
      coverage_minimum: 95           # ✅ From payment_gateway (overridden twice!)
      coverage_target: 100

  coding:                            # ✅ From python_standards + payment_gateway
    style_guide: "PEP 8"
    max_complexity: 7                # ✅ From payment_gateway
    linting:
      tools:
        - "pylint"
        - "black"
        - "mypy"

  testing:                           # ✅ From python_standards + payment_gateway
    framework: "pytest"
    coverage_minimum: 95             # ✅ From payment_gateway (highest priority)

security:                            # ✅ From payment_gateway
  pci_dss:
    level: "Level 1"
```

---

## Summary

### To Create Your Merge Tuple

1. **Set `base_projects` in each project.json**
2. **Order matters**: Array order = merge priority
3. **System resolves dependencies** automatically
4. **Result**: Clean inheritance chain

### Your Specific Changes

```bash
# 1. Edit python_standards/project.json
"base_projects": ["ai_init_methodology"]

# 2. Edit payment_gateway/project.json
"base_projects": ["ai_init_methodology", "python_standards"]

# 3. Load and verify
/load-context payment_gateway
/show-full-context
```

### Merge Order

```
Priority 0: ai_init_methodology    (lowest - baseline)
Priority 1: python_standards       (middle - adds Python specifics)
Priority 2: payment_gateway        (highest - wins all conflicts)
```

**That's your tuple!** 🎯

---

*See also: [MERGE_KEYS_EXPLAINED.md](MERGE_KEYS_EXPLAINED.md) for merge behavior details*
