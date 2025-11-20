# AI SDLC v3.0: Implementation Plan

**Status**: Implementation Roadmap
**Date**: 2025-11-20
**Based on**: [AI_SDLC_UX_DESIGN.md](AI_SDLC_UX_DESIGN.md)

---

## Overview

Transform v2.0 monolithic plugin into v3.0 modular, skills-based architecture with homeostatic orchestration.

---

## Complete File Structure

```
AI_SDLC_Context/
├── plugins/
│   ├── aisdlc-core/                           # 🏗️ Foundation (PHASE 1)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── requirement-traceability/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── req-key-patterns.yml
│   │   │   ├── check-requirement-coverage/
│   │   │   │   └── SKILL.md
│   │   │   └── propagate-req-keys/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── requirements-skills/                   # 📋 Requirements (PHASE 2)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── requirement-extraction/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── templates/
│   │   │   │       ├── functional-req.md
│   │   │   │       ├── nfr-req.md
│   │   │   │       └── data-req.md
│   │   │   ├── disambiguate-requirements/
│   │   │   │   └── SKILL.md
│   │   │   ├── extract-business-rules/
│   │   │   │   └── SKILL.md
│   │   │   ├── extract-constraints/
│   │   │   │   └── SKILL.md
│   │   │   ├── extract-formulas/
│   │   │   │   └── SKILL.md
│   │   │   ├── refine-requirements/
│   │   │   │   └── SKILL.md
│   │   │   ├── create-traceability-matrix/
│   │   │   │   └── SKILL.md
│   │   │   └── validate-requirements/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── design-skills/                         # 🎨 Design (PHASE 3)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── design-with-traceability/
│   │   │   │   └── SKILL.md
│   │   │   ├── create-adrs/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── templates/
│   │   │   │       └── adr-template.md
│   │   │   └── validate-design-coverage/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── code-tdd-skills/                       # 💻 Code - TDD (PHASE 4)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── tdd-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── red-phase/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── templates/
│   │   │   │       ├── test-template-python.py
│   │   │   │       ├── test-template-typescript.ts
│   │   │   │       └── test-template-java.java
│   │   │   ├── green-phase/
│   │   │   │   └── SKILL.md
│   │   │   ├── refactor-phase/
│   │   │   │   └── SKILL.md
│   │   │   └── commit-with-req-tag/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── code-bdd-skills/                       # 💻 Code - BDD (PHASE 5)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── bdd-workflow/
│   │   │   │   └── SKILL.md
│   │   │   ├── write-scenario/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── templates/
│   │   │   │       └── gherkin-template.feature
│   │   │   ├── implement-step-definitions/
│   │   │   │   └── SKILL.md
│   │   │   ├── implement-feature/
│   │   │   │   └── SKILL.md
│   │   │   └── refactor-bdd/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── code-generation-skills/                # 🤖 Code Generation (PHASE 6)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── autogenerate-from-business-rules/
│   │   │   │   └── SKILL.md
│   │   │   ├── autogenerate-validators/
│   │   │   │   └── SKILL.md
│   │   │   ├── autogenerate-constraints/
│   │   │   │   └── SKILL.md
│   │   │   └── autogenerate-formulas/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── testing-skills/                        # 🧪 Testing (PHASE 7)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── validate-test-coverage/
│   │   │   │   └── SKILL.md
│   │   │   ├── generate-missing-tests/
│   │   │   │   └── SKILL.md
│   │   │   ├── run-integration-tests/
│   │   │   │   └── SKILL.md
│   │   │   └── create-coverage-report/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── runtime-skills/                        # 🚀 Runtime (PHASE 8)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── telemetry-tagging/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── templates/
│   │   │   │       ├── logging-template-python.py
│   │   │   │       ├── logging-template-typescript.ts
│   │   │   │       ├── metrics-template-datadog.yml
│   │   │   │       └── metrics-template-prometheus.yml
│   │   │   ├── create-observability-config/
│   │   │   │   └── SKILL.md
│   │   │   └── trace-production-issue/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   ├── principles-key/                        # 📖 Key Principles (PHASE 9)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── apply-key-principles/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── principles/
│   │   │   │       └── KEY_PRINCIPLES.md
│   │   │   └── seven-questions-checklist/
│   │   │       └── SKILL.md
│   │   ├── README.md
│   │   └── CHANGELOG.md
│   │
│   └── bundles/                               # 🎯 Plugin Bundles (PHASE 10)
│       ├── startup-bundle/
│       │   ├── .claude-plugin/
│       │   │   └── plugin.json
│       │   └── README.md
│       ├── enterprise-bundle/
│       │   ├── .claude-plugin/
│       │   │   └── plugin.json
│       │   └── README.md
│       ├── qa-bundle/
│       │   ├── .claude-plugin/
│       │   │   └── plugin.json
│       │   └── README.md
│       └── datascience-bundle/
│           ├── .claude-plugin/
│           │   └── plugin.json
│           └── README.md
│
├── examples/
│   ├── quickstart/                            # Quick start examples
│   │   ├── startup-example/
│   │   │   ├── .claude/
│   │   │   │   └── plugins.yml
│   │   │   ├── README.md
│   │   │   └── walkthrough.md
│   │   ├── enterprise-example/
│   │   │   ├── .claude/
│   │   │   │   └── plugins.yml
│   │   │   ├── README.md
│   │   │   └── walkthrough.md
│   │   └── bdd-example/
│   │       ├── .claude/
│   │       │   └── plugins.yml
│   │       ├── README.md
│   │       └── walkthrough.md
│   │
│   └── workflows/                             # Complete workflow examples
│       ├── requirements-refinement-loop/
│       │   ├── initial-requirements.md
│       │   ├── discovered-requirements.md
│       │   ├── refined-requirements.md
│       │   └── README.md
│       ├── homeostasis-demo/
│       │   ├── deviation-detected.md
│       │   ├── correction-applied.md
│       │   ├── homeostasis-achieved.md
│       │   └── README.md
│       └── code-autogeneration/
│           ├── business-rules.md
│           ├── generated-code.py
│           ├── generated-tests.py
│           └── README.md
│
├── docs/
│   ├── AI_SDLC_UX_DESIGN.md                   # ⭐ Master UX design
│   ├── IMPLEMENTATION_PLAN.md                 # ⭐ This file
│   ├── ai_sdlc_method.md                      # v1.2 methodology
│   ├── ai_sdlc_overview.md                    # High-level overview
│   ├── ai_sdlc_concepts.md                    # Concept inventory
│   ├── ai_sdlc_appendices.md                  # Technical appendices
│   │
│   ├── guides/                                # Implementation guides
│   │   ├── PLUGIN_DEVELOPMENT_GUIDE.md
│   │   ├── SKILL_DEVELOPMENT_GUIDE.md
│   │   ├── HOMEOSTASIS_GUIDE.md
│   │   ├── REQUIREMENTS_REFINEMENT_GUIDE.md
│   │   ├── CODE_AUTOGENERATION_GUIDE.md
│   │   └── README.md
│   │
│   └── deprecated/                            # Archive
│       ├── MODULAR_PLUGIN_ARCHITECTURE.md
│       ├── MODULAR_SKILLS_ARCHITECTURE.md
│       └── ...
│
├── tests/                                     # Plugin tests (NEW)
│   ├── core/
│   │   ├── test_requirement_traceability.py
│   │   ├── test_check_coverage.py
│   │   └── test_propagate_keys.py
│   ├── requirements/
│   │   ├── test_requirement_extraction.py
│   │   ├── test_disambiguate.py
│   │   └── test_refine_requirements.py
│   ├── code-tdd/
│   │   ├── test_tdd_workflow.py
│   │   ├── test_red_phase.py
│   │   └── test_green_phase.py
│   └── integration/
│       ├── test_startup_bundle.py
│       ├── test_enterprise_bundle.py
│       └── test_homeostasis.py
│
├── .claude/                                   # Project config
│   └── plugins.yml                            # Development plugins
│
├── README.md                                  # Main README
├── QUICKSTART.md                              # Quick start guide
├── PLUGIN_GUIDE.md                            # Plugin creation guide
├── CLAUDE.md                                  # Project context for Claude
└── CHANGELOG.md                               # Version history
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)

**Goal**: Create `@aisdlc/aisdlc-core` with traceability foundation

**Files to Create**:
```
plugins/aisdlc-core/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── requirement-traceability/
│   │   ├── SKILL.md
│   │   └── req-key-patterns.yml
│   ├── check-requirement-coverage/
│   │   └── SKILL.md
│   └── propagate-req-keys/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ 3 foundation skills working
- ✅ REQ-* key patterns defined
- ✅ Can tag code/commits/tests with REQ-*
- ✅ Can detect coverage gaps (sensor)

**Test**:
```bash
claude install plugins/aisdlc-core
claude skills list
# Should show: requirement-traceability, check-requirement-coverage, propagate-req-keys
```

---

### Phase 2: Requirements Skills (Week 2)

**Goal**: Create `@aisdlc/requirements-skills` with extraction + refinement

**Files to Create**:
```
plugins/requirements-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── requirement-extraction/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── functional-req.md
│   │       ├── nfr-req.md
│   │       └── data-req.md
│   ├── disambiguate-requirements/      # ⭐ NEW
│   │   └── SKILL.md
│   ├── extract-business-rules/         # ⭐ NEW
│   │   └── SKILL.md
│   ├── extract-constraints/            # ⭐ NEW
│   │   └── SKILL.md
│   ├── extract-formulas/               # ⭐ NEW
│   │   └── SKILL.md
│   ├── refine-requirements/            # ⭐ NEW (feedback loop)
│   │   └── SKILL.md
│   ├── create-traceability-matrix/
│   │   └── SKILL.md
│   └── validate-requirements/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Extract REQ-F-*, REQ-NFR-*, REQ-DATA-*, REQ-BR-*
- ✅ Disambiguate into BR-*, C-*, F-*
- ✅ Refine requirements from TDD discoveries
- ✅ Create traceability matrix (INT-* → REQ-*)

**Test**:
```bash
claude install plugins/requirements-skills
# Test: "Create requirements for user authentication"
# Should extract: REQ-F-AUTH-001 with BR-*, C-*, F-*
```

---

### Phase 3: Design Skills (Week 3)

**Goal**: Create `@aisdlc/design-skills` with ADRs

**Files to Create**:
```
plugins/design-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── design-with-traceability/
│   │   └── SKILL.md
│   ├── create-adrs/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       └── adr-template.md
│   └── validate-design-coverage/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Design components tagged with REQ-*
- ✅ Create ADRs acknowledging E(t)
- ✅ Validate all requirements have design

---

### Phase 4: Code TDD Skills (Week 4)

**Goal**: Create `@aisdlc/code-tdd-skills` with RED→GREEN→REFACTOR

**Files to Create**:
```
plugins/code-tdd-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── tdd-workflow/
│   │   └── SKILL.md
│   ├── red-phase/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── test-template-python.py
│   │       ├── test-template-typescript.ts
│   │       └── test-template-java.java
│   ├── green-phase/
│   │   └── SKILL.md
│   ├── refactor-phase/
│   │   └── SKILL.md
│   └── commit-with-req-tag/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Complete TDD workflow
- ✅ RED: Write failing tests tagged with REQ-*
- ✅ GREEN: Implement code tagged with REQ-*
- ✅ REFACTOR: Improve quality
- ✅ COMMIT: Tag commits with REQ-*

**Test**:
```bash
claude install plugins/code-tdd-skills
# Test: "Implement REQ-F-AUTH-001 using TDD"
# Should follow RED → GREEN → REFACTOR → COMMIT
```

---

### Phase 5: Code BDD Skills (Week 5)

**Goal**: Create `@aisdlc/code-bdd-skills` with Gherkin scenarios

**Files to Create**:
```
plugins/code-bdd-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── bdd-workflow/
│   │   └── SKILL.md
│   ├── write-scenario/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       └── gherkin-template.feature
│   ├── implement-step-definitions/
│   │   └── SKILL.md
│   ├── implement-feature/
│   │   └── SKILL.md
│   └── refactor-bdd/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ BDD workflow (SCENARIO → STEP DEF → IMPLEMENT)
- ✅ Gherkin scenarios tagged with REQ-*
- ✅ Step definitions
- ✅ Feature implementation

---

### Phase 6: Code Generation Skills (Week 6)

**Goal**: Create `@aisdlc/code-generation-skills` for autogeneration from BR-*/C-*/F-*

**Files to Create**:
```
plugins/code-generation-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── autogenerate-from-business-rules/
│   │   └── SKILL.md
│   ├── autogenerate-validators/
│   │   └── SKILL.md
│   ├── autogenerate-constraints/
│   │   └── SKILL.md
│   └── autogenerate-formulas/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Autogenerate validation code from BR-*
- ✅ Autogenerate constraint checks from C-*
- ✅ Autogenerate formula implementations from F-*

**Example**:
```yaml
Input:
  BR-001: Email regex ^[a-zA-Z0-9._%+-]+@...
  BR-002: Password min 12 chars

Output (autogenerated):
  EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@..."
  def validate_password(pwd): return len(pwd) >= 12
```

---

### Phase 7: Testing Skills (Week 7)

**Goal**: Create `@aisdlc/testing-skills` with coverage validation

**Files to Create**:
```
plugins/testing-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── validate-test-coverage/
│   │   └── SKILL.md
│   ├── generate-missing-tests/
│   │   └── SKILL.md
│   ├── run-integration-tests/
│   │   └── SKILL.md
│   └── create-coverage-report/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Detect REQ-* without tests (sensor)
- ✅ Auto-generate missing tests (actuator)
- ✅ Run integration tests
- ✅ Coverage report with REQ-* mapping

---

### Phase 8: Runtime Skills (Week 8)

**Goal**: Create `@aisdlc/runtime-skills` with telemetry + feedback loop

**Files to Create**:
```
plugins/runtime-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── telemetry-tagging/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── logging-template-python.py
│   │       ├── logging-template-typescript.ts
│   │       ├── metrics-template-datadog.yml
│   │       └── metrics-template-prometheus.yml
│   ├── create-observability-config/
│   │   └── SKILL.md
│   └── trace-production-issue/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Tag logs/metrics with REQ-*
- ✅ Setup observability (Datadog, Splunk, etc.)
- ✅ Trace production alerts → REQ-* → INT-*
- ✅ Close feedback loop

---

### Phase 9: Principles Skills (Week 9)

**Goal**: Create `@aisdlc/principles-key` with Key Principles

**Files to Create**:
```
plugins/principles-key/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── apply-key-principles/
│   │   ├── SKILL.md
│   │   └── principles/
│   │       └── KEY_PRINCIPLES.md
│   └── seven-questions-checklist/
│       └── SKILL.md
├── README.md
└── CHANGELOG.md
```

**Deliverables**:
- ✅ Enforce 7 Key Principles
- ✅ Seven Questions Checklist (sensor)
- ✅ Block coding if principles violated

---

### Phase 10: Bundles (Week 10)

**Goal**: Create plugin bundles for different use cases

**Files to Create**:
```
plugins/bundles/
├── startup-bundle/
│   ├── .claude-plugin/plugin.json
│   └── README.md
├── enterprise-bundle/
│   ├── .claude-plugin/plugin.json
│   └── README.md
├── qa-bundle/
│   ├── .claude-plugin/plugin.json
│   └── README.md
└── datascience-bundle/
    ├── .claude-plugin/plugin.json
    └── README.md
```

**Bundle Definitions**:

**startup-bundle**:
```json
{
  "name": "@aisdlc/startup-bundle",
  "dependencies": [
    "@aisdlc/aisdlc-core",
    "@aisdlc/code-tdd-skills",
    "@aisdlc/principles-key"
  ]
}
```

**enterprise-bundle**:
```json
{
  "name": "@aisdlc/enterprise-bundle",
  "dependencies": [
    "@aisdlc/aisdlc-core",
    "@aisdlc/requirements-skills",
    "@aisdlc/design-skills",
    "@aisdlc/code-tdd-skills",
    "@aisdlc/testing-skills",
    "@aisdlc/runtime-skills",
    "@aisdlc/principles-key"
  ]
}
```

---

## Key File Templates

### Plugin Manifest Template

```json
// plugins/<plugin-name>/.claude-plugin/plugin.json
{
  "name": "@aisdlc/<plugin-name>",
  "version": "1.0.0",
  "description": "...",
  "author": "AI SDLC Project",
  "license": "MIT",
  "homepage": "https://github.com/foolishimp/AI_SDLC_Context",
  "skills": {
    "enabled": true,
    "paths": ["skills/"]
  }
}
```

### Skill Template

```yaml
---
name: skill-name
description: Brief description (Claude uses this to decide when to invoke)
allowed-tools: [Read, Write, Edit, Bash]
---

# Skill Name

Detailed description of what this skill does.

## Type

Sensor | Actuator | Orchestrator

## Prerequisites

- Requirement 1 (e.g., "REQ-* keys must exist")
- Requirement 2

## Uses Skills

- skill-1 (for capability X)
- skill-2 (for capability Y)

## Workflow

1. Step 1
2. Step 2
3. Step 3

## Homeostasis Behavior

If prerequisites missing:
1. Detect: What's missing
2. Signal: "Need X first"
3. Claude invokes: prerequisite-skill
4. Retry: this skill

## Output

- Output 1
- Output 2

## Example

```
Input: ...
Output: ...
```
```

---

## Testing Strategy

### Unit Tests

```python
# tests/core/test_requirement_traceability.py
def test_req_key_pattern_functional():
    pattern = get_req_pattern("functional")
    assert pattern == "REQ-F-{DOMAIN}-{ID}"

def test_req_key_validation():
    assert is_valid_req_key("REQ-F-AUTH-001") == True
    assert is_valid_req_key("INVALID") == False
```

### Integration Tests

```python
# tests/integration/test_startup_bundle.py
def test_startup_bundle_workflow():
    # Install bundle
    install_plugins(["@aisdlc/startup-bundle"])

    # Test TDD workflow
    result = invoke_skill("tdd-workflow", {
        "requirement": "REQ-F-TEST-001"
    })

    assert result.success == True
    assert result.coverage >= 80
    assert result.commits_tagged == True
```

### Homeostasis Tests

```python
# tests/integration/test_homeostasis.py
def test_coverage_deviation_correction():
    # Setup: Code with 50% coverage
    setup_code_with_coverage(50)

    # Sensor: Detect deviation
    deviation = invoke_skill("validate-test-coverage")
    assert deviation.coverage < 80

    # Actuator: Generate missing tests
    result = invoke_skill("generate-missing-tests")

    # Verify: Coverage improved
    final_coverage = invoke_skill("validate-test-coverage")
    assert final_coverage.coverage >= 80
```

---

## Migration from v2.0.0

### Current State (v2.0.0)

```
plugins/aisdlc-methodology/  (MONOLITHIC)
├── config/
│   ├── config.yml           # Key Principles + Code stage
│   └── stages_config.yml    # All 7 stages
```

### Migration Strategy

1. **Keep v2.0.0 plugin** for backward compatibility
2. **Extract skills** into new plugins
3. **Mark v2.0.0 as deprecated**
4. **Provide migration guide**

### Migration Guide

```markdown
# Migrating from v2.0.0 to v3.0.0

## Before (v2.0.0)
```yaml
plugins:
  - "@aisdlc/aisdlc-methodology"  # Monolithic
```

## After (v3.0.0 - Minimal)
```yaml
plugins:
  - "@aisdlc/startup-bundle"  # Core + TDD + Principles
```

## After (v3.0.0 - Full)
```yaml
plugins:
  - "@aisdlc/enterprise-bundle"  # All 7 stages
```

## Breaking Changes
- Skills-based instead of config-based
- Autonomous orchestration instead of prescriptive workflow
- Requirements refinement loop (new)
- Code autogeneration from BR-*/C-*/F-* (new)
```

---

## Documentation Files

### Development Guides

```
docs/guides/
├── PLUGIN_DEVELOPMENT_GUIDE.md           # How to create plugins
├── SKILL_DEVELOPMENT_GUIDE.md            # How to create skills
├── HOMEOSTASIS_GUIDE.md                  # How homeostasis works
├── REQUIREMENTS_REFINEMENT_GUIDE.md      # BR-*/C-*/F-* workflow
├── CODE_AUTOGENERATION_GUIDE.md          # Autogenerate from requirements
└── README.md                             # Guide index
```

### Example Workflows

```
examples/workflows/
├── requirements-refinement-loop/
│   ├── initial-requirements.md           # Vague requirements
│   ├── discovered-requirements.md        # Edge cases found during TDD
│   ├── refined-requirements.md           # Updated with BR-*
│   └── README.md
├── homeostasis-demo/
│   ├── deviation-detected.md             # Coverage gap found
│   ├── correction-applied.md             # Tests generated
│   ├── homeostasis-achieved.md           # 100% coverage
│   └── README.md
└── code-autogeneration/
    ├── business-rules.md                 # BR-*, C-*, F-*
    ├── generated-code.py                 # Autogenerated code
    ├── generated-tests.py                # Autogenerated tests
    └── README.md
```

---

## Success Criteria

### Phase 1-2 (Foundation + Requirements)
- ✅ Can extract REQ-* from intent
- ✅ Can disambiguate into BR-*, C-*, F-*
- ✅ Can detect coverage gaps
- ✅ Can refine requirements from discoveries

### Phase 4-5 (Code Skills)
- ✅ TDD workflow works end-to-end
- ✅ BDD workflow works end-to-end
- ✅ Code/commits/tests tagged with REQ-*

### Phase 6 (Code Generation)
- ✅ Can autogenerate validators from BR-*
- ✅ Can autogenerate constraint checks from C-*
- ✅ Can autogenerate formula implementations from F-*

### Phase 7-8 (Testing + Runtime)
- ✅ Can detect missing tests
- ✅ Can generate missing tests
- ✅ Can tag telemetry with REQ-*
- ✅ Can trace production alerts → REQ-* → INT-*

### Phase 9-10 (Principles + Bundles)
- ✅ Seven Questions Checklist works
- ✅ Bundles install correctly
- ✅ Startup/Enterprise/QA workflows work

### Overall
- ✅ Homeostasis converges to 100% coverage
- ✅ Requirements refinement loop works
- ✅ Autonomous orchestration (no prescriptive workflow)
- ✅ Complete traceability (Intent → Runtime → Feedback)

---

## Timeline

- **Week 1**: Phase 1 (Core)
- **Week 2**: Phase 2 (Requirements)
- **Week 3**: Phase 3 (Design)
- **Week 4**: Phase 4 (Code TDD)
- **Week 5**: Phase 5 (Code BDD)
- **Week 6**: Phase 6 (Code Generation)
- **Week 7**: Phase 7 (Testing)
- **Week 8**: Phase 8 (Runtime)
- **Week 9**: Phase 9 (Principles)
- **Week 10**: Phase 10 (Bundles)

**Total**: 10 weeks (~2.5 months)

---

## Next Steps

1. **Validate UX Design** - Review [AI_SDLC_UX_DESIGN.md](AI_SDLC_UX_DESIGN.md) with stakeholders
2. **Prototype Phase 1** - Build `@aisdlc/aisdlc-core` plugin
3. **Test with Real Users** - Sarah, David, Maria, James personas
4. **Iterate** - Refine based on feedback
5. **Continue Phases 2-10** - Build remaining plugins

---

**"Excellence or nothing"** 🔥
