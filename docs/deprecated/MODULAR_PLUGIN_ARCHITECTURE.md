# Modular Plugin Architecture for AI SDLC

**Status**: Proposal
**Date**: 2025-11-20
**Version**: 3.0.0 (Breaking change from v2.0.0)

---

## Executive Summary

Refactor the monolithic `aisdlc-methodology` plugin into **composable, decoupled plugins** that teams can mix-and-match based on their needs.

### Goals

1. **Modularity**: Each SDLC stage is a separate plugin
2. **Swappable Implementations**: Teams can choose TDD vs BDD vs REPL-driven approaches
3. **Principle Packs**: Mix different principle sets (Key Principles, 12-Factor, Clean Arch, DDD)
4. **Skills System**: Reusable agent capabilities across stages
5. **Experimentation**: Easy A/B testing of different methodologies
6. **Team Autonomy**: Teams control their own methodology evolution

---

## Current State (v2.0.0)

### Problems

```
aisdlc-methodology v2.0.0 (MONOLITHIC)
├── All 7 stages bundled together
├── TDD hardcoded as the only code approach
├── Key Principles hardcoded
├── Cannot swap individual stages
├── Cannot experiment with variations
└── Teams must fork to customize
```

**Issues**:
- ❌ **Inflexible**: Can't swap TDD for BDD-first
- ❌ **Coupled**: Changing Code stage requires forking entire plugin
- ❌ **No Experimentation**: Can't A/B test classic TDD vs AI-pair TDD
- ❌ **One-Size-Fits-All**: Different teams have different needs

---

## Proposed State (v3.0.0)

### Architecture

```
@aisdlc Marketplace (Composable Plugins)

┌─────────────────────────────────────────────────────────────┐
│  CORE PLUGINS (Orchestration)                               │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/sdlc-core                                          │
│    - Requirement key traceability (REQ-F-*, REQ-NFR-*)      │
│    - Stage orchestration framework                          │
│    - Feedback loop management                               │
│    - Observability hooks                                    │
│                                                             │
│  @aisdlc/intent-manager                                     │
│    - Intent lifecycle (INT-* → REQ-*)                       │
│    - Intent → Requirements transformation                   │
│    - Production feedback → New intents                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  STAGE PLUGINS (Modular Stages)                             │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/stage-requirements  (Section 4.0)                  │
│  @aisdlc/stage-design        (Section 5.0)                  │
│  @aisdlc/stage-tasks         (Section 6.0)                  │
│  @aisdlc/stage-code          (Section 7.0 - ABSTRACT)       │
│  @aisdlc/stage-system-test   (Section 8.0)                  │
│  @aisdlc/stage-uat           (Section 9.0)                  │
│  @aisdlc/stage-runtime-feedback (Section 10.0)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CODE STAGE IMPLEMENTATIONS (Swappable)                     │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/code-tdd-classic                                   │
│    - RED → GREEN → REFACTOR → COMMIT                        │
│    - Tests first, always                                    │
│    - Classic TDD workflow                                   │
│                                                             │
│  @aisdlc/code-tdd-ai-pair                                   │
│    - RED → GREEN (AI suggests) → REFACTOR → COMMIT          │
│    - AI pair programming during GREEN phase                 │
│    - Test generation assistance                             │
│                                                             │
│  @aisdlc/code-bdd-first                                     │
│    - SCENARIO (Gherkin) → STEP DEF → IMPLEMENT → REFACTOR   │
│    - BDD scenarios before code                              │
│    - Outside-in development                                 │
│                                                             │
│  @aisdlc/code-literate                                      │
│    - DOCUMENT → EXTRACT → TEST → REFACTOR                   │
│    - Literate programming (Donald Knuth)                    │
│    - Documentation-driven development                       │
│                                                             │
│  @aisdlc/code-repl-driven                                   │
│    - REPL → EXPLORE → EXTRACT → TEST                        │
│    - REPL-driven development (Lisp, Clojure style)          │
│    - Interactive development                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRINCIPLE PACKS (Mix & Match)                              │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/principles-key                                     │
│    - The 7 Key Principles                                   │
│    - TDD, Fail Fast, Modular, Reuse, OSS, No Debt, Excellence│
│                                                             │
│  @aisdlc/principles-12factor                                │
│    - 12-Factor App methodology                              │
│    - Cloud-native principles                                │
│                                                             │
│  @aisdlc/principles-clean-arch                              │
│    - Clean Architecture (Uncle Bob)                         │
│    - Dependency inversion, SOLID                            │
│                                                             │
│  @aisdlc/principles-ddd                                     │
│    - Domain-Driven Design                                   │
│    - Bounded contexts, aggregates, entities                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TESTING STRATEGY PLUGINS                                   │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/testing-tdd       # TDD testing strategy           │
│  @aisdlc/testing-bdd       # BDD testing strategy           │
│  @aisdlc/testing-property  # Property-based testing         │
│  @aisdlc/testing-mutation  # Mutation testing               │
│  @aisdlc/testing-contract  # Contract testing (Pact)        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  SKILLS (Reusable Agent Capabilities)                       │
├─────────────────────────────────────────────────────────────┤
│  @aisdlc/skill-requirement-extraction                       │
│  @aisdlc/skill-code-review                                  │
│  @aisdlc/skill-refactoring                                  │
│  @aisdlc/skill-test-generation                              │
│  @aisdlc/skill-architecture-validation                      │
│  @aisdlc/skill-semantic-search                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Plugin Composition Examples

### Example 1: Strict TDD Team (Backend Services)

```yaml
# .claude/plugins.yml
plugins:
  # Core orchestration
  - @aisdlc/sdlc-core
  - @aisdlc/intent-manager

  # All 7 stages
  - @aisdlc/stage-requirements
  - @aisdlc/stage-design
  - @aisdlc/stage-tasks
  - @aisdlc/stage-system-test
  - @aisdlc/stage-uat
  - @aisdlc/stage-runtime-feedback

  # Classic TDD for Code stage
  - @aisdlc/code-tdd-classic

  # Principles
  - @aisdlc/principles-key
  - @aisdlc/principles-clean-arch

  # Testing
  - @aisdlc/testing-tdd

  # Language standards
  - @aisdlc/python-standards

  # Skills
  - @aisdlc/skill-code-review
  - @aisdlc/skill-refactoring
```

**Result**: Classic TDD with Clean Architecture, full 7-stage SDLC

---

### Example 2: Experimental Team (Frontend)

```yaml
# .claude/plugins.yml
plugins:
  # Core only (minimal)
  - @aisdlc/sdlc-core

  # Minimal stages (skip Requirements, Design, Tasks)
  - @aisdlc/stage-system-test

  # BDD-first for Code stage
  - @aisdlc/code-bdd-first

  # Testing
  - @aisdlc/testing-bdd
  - @aisdlc/testing-property

  # Language standards
  - @aisdlc/typescript-standards

  # Skills
  - @aisdlc/skill-test-generation
```

**Result**: BDD-first development with property testing, minimal SDLC stages

---

### Example 3: Startup (Move Fast)

```yaml
# .claude/plugins.yml
plugins:
  # Core only
  - @aisdlc/sdlc-core

  # Code stage only (AI-assisted)
  - @aisdlc/code-tdd-ai-pair

  # Principles (relaxed)
  - @aisdlc/principles-12factor

  # Testing (minimal)
  - @aisdlc/testing-tdd

  # Language standards
  - @aisdlc/python-standards
```

**Result**: Fast iteration with AI pair programming, minimal overhead

---

### Example 4: Enterprise (Full Governance)

```yaml
# .claude/plugins.yml
plugins:
  # Core
  - @aisdlc/sdlc-core
  - @aisdlc/intent-manager

  # ALL 7 stages (mandatory)
  - @aisdlc/stage-requirements
  - @aisdlc/stage-design
  - @aisdlc/stage-tasks
  - @aisdlc/stage-system-test
  - @aisdlc/stage-uat
  - @aisdlc/stage-runtime-feedback

  # Classic TDD (strict)
  - @aisdlc/code-tdd-classic

  # Principles (all of them)
  - @aisdlc/principles-key
  - @aisdlc/principles-clean-arch
  - @aisdlc/principles-ddd

  # Testing (comprehensive)
  - @aisdlc/testing-tdd
  - @aisdlc/testing-bdd
  - @aisdlc/testing-contract
  - @aisdlc/testing-mutation

  # Language standards
  - @aisdlc/java-standards

  # Skills (governance)
  - @aisdlc/skill-requirement-extraction
  - @aisdlc/skill-code-review
  - @aisdlc/skill-architecture-validation
```

**Result**: Full governance, all stages, comprehensive testing

---

## Plugin Interface Specifications

### Core Plugin: `@aisdlc/sdlc-core`

**Purpose**: Orchestration framework + requirement traceability

**Exports**:
```yaml
ai_sdlc_core:
  version: "3.0.0"

  # Requirement key management
  requirement_keys:
    patterns:
      functional: "REQ-F-*"
      non_functional: "REQ-NFR-*"
      data_quality: "REQ-DATA-*"
      business_rules: "REQ-BR-*"

    traceability:
      enabled: true
      propagate_to_commits: true
      propagate_to_telemetry: true

  # Stage orchestration
  stage_orchestration:
    enabled: true
    stages_required: []  # Empty = teams choose
    feedback_loop: true

  # Hooks (for stage plugins to register)
  hooks:
    pre_stage: []
    post_stage: []
    on_requirement_created: []
    on_requirement_traced: []
```

---

### Stage Plugin Interface: `@aisdlc/stage-*`

**Example**: `@aisdlc/stage-requirements`

```yaml
stage:
  name: "requirements"
  section: "4.0"

  agent:
    role: "Requirements Agent"
    purpose: "Transform intent into structured requirements with unique keys"

    responsibilities:
      - "Parse raw intent"
      - "Generate requirement keys"
      - "Create traceability matrix"

    constraints:
      - "Every requirement must have unique immutable key"
      - "Keys follow REQ-* pattern"

  inputs:
    - type: "intent"
      from: "intent_manager"

  outputs:
    - type: "requirements"
      keys: ["REQ-F-*", "REQ-NFR-*", "REQ-DATA-*"]

  quality_gates:
    - "All requirements have unique keys"
    - "All requirements have acceptance criteria"
    - "Traceability matrix created"

  # Hooks this stage registers
  hooks:
    - on_requirement_created: "propagate_to_next_stage"
```

---

### Code Stage Interface: `@aisdlc/code-*`

**Example**: `@aisdlc/code-tdd-classic`

```yaml
code_stage_implementation:
  name: "code-tdd-classic"
  variant: "Classic TDD"

  workflow:
    name: "RED → GREEN → REFACTOR → COMMIT"

    steps:
      - name: "RED"
        description: "Write failing test"
        agent_instructions: |
          1. Read the work unit from Tasks stage
          2. Write a failing unit test for the requirement
          3. Ensure test fails for the right reason
          4. Commit: "RED: Add test for REQ-<key>"

      - name: "GREEN"
        description: "Make test pass with minimal code"
        agent_instructions: |
          1. Write minimal code to make test pass
          2. No refactoring yet
          3. Run test and ensure it passes
          4. Commit: "GREEN: Implement REQ-<key>"

      - name: "REFACTOR"
        description: "Improve code quality"
        agent_instructions: |
          1. Refactor for clarity and maintainability
          2. Ensure tests still pass
          3. Apply SOLID principles
          4. Commit: "REFACTOR: Improve REQ-<key>"

      - name: "COMMIT"
        description: "Final commit with requirement tag"
        agent_instructions: |
          1. Squash commits if needed
          2. Tag commit with requirement key
          3. Update traceability matrix

  quality_gates:
    - "Test coverage >= 80%"
    - "All tests pass"
    - "Code tagged with requirement keys"

  dependencies:
    - "@aisdlc/sdlc-core"
    - "@aisdlc/testing-tdd"
```

**Example**: `@aisdlc/code-bdd-first`

```yaml
code_stage_implementation:
  name: "code-bdd-first"
  variant: "BDD-First Development"

  workflow:
    name: "SCENARIO → STEP DEF → IMPLEMENT → REFACTOR"

    steps:
      - name: "SCENARIO"
        description: "Write Gherkin scenario"
        agent_instructions: |
          Feature: <Requirement REQ-F-*>

          Scenario: <Business scenario>
            Given <precondition>
            When <action>
            Then <expected outcome>

      - name: "STEP DEF"
        description: "Implement step definitions"
        agent_instructions: |
          @given("precondition")
          def step_impl(context):
              # Not yet implemented
              pass

      - name: "IMPLEMENT"
        description: "Implement production code"
        agent_instructions: |
          Implement the actual feature to make scenario pass

      - name: "REFACTOR"
        description: "Clean up code"
        agent_instructions: |
          Refactor both step definitions and production code

  quality_gates:
    - "All scenarios pass"
    - "Scenarios map to requirements"

  dependencies:
    - "@aisdlc/sdlc-core"
    - "@aisdlc/testing-bdd"
```

---

## Skills System

### Skill Interface

**Example**: `@aisdlc/skill-code-review`

```yaml
skill:
  name: "code-review"
  version: "1.0.0"

  description: "Automated code review skill"

  capabilities:
    - "Detect code smells"
    - "Check SOLID violations"
    - "Verify test coverage"
    - "Validate requirement tags"

  usage:
    # Any stage can invoke this skill
    invoke_from:
      - "stage-code"
      - "stage-design"

  configuration:
    rules:
      - "No functions > 50 lines"
      - "No classes > 300 lines"
      - "No cyclomatic complexity > 10"

    fail_build_on:
      - "Missing requirement tags"
      - "Coverage < 80%"
```

**Usage in Code Stage**:
```yaml
# @aisdlc/code-tdd-classic
workflow:
  steps:
    - name: "REFACTOR"
      skills:
        - "@aisdlc/skill-code-review"  # Invoke skill
        - "@aisdlc/skill-refactoring"
```

---

## Migration Path from v2.0.0 → v3.0.0

### Phase 1: Create Core Plugins (Week 1-2)

1. Extract `@aisdlc/sdlc-core` from `aisdlc-methodology`
2. Extract `@aisdlc/intent-manager`
3. Test orchestration framework

### Phase 2: Split Stage Plugins (Week 3-4)

1. Create `@aisdlc/stage-requirements`
2. Create `@aisdlc/stage-design`
3. Create `@aisdlc/stage-tasks`
4. Create abstract `@aisdlc/stage-code`
5. Create `@aisdlc/stage-system-test`
6. Create `@aisdlc/stage-uat`
7. Create `@aisdlc/stage-runtime-feedback`

### Phase 3: Code Stage Implementations (Week 5-6)

1. Create `@aisdlc/code-tdd-classic` (from existing)
2. Create `@aisdlc/code-tdd-ai-pair` (new variant)
3. Create `@aisdlc/code-bdd-first` (new variant)

### Phase 4: Principle Packs (Week 7)

1. Extract `@aisdlc/principles-key`
2. Create `@aisdlc/principles-12factor`
3. Create `@aisdlc/principles-clean-arch`

### Phase 5: Testing Strategies (Week 8)

1. Create `@aisdlc/testing-tdd`
2. Create `@aisdlc/testing-bdd`
3. Create `@aisdlc/testing-property`

### Phase 6: Skills System (Week 9-10)

1. Create `@aisdlc/skill-code-review`
2. Create `@aisdlc/skill-refactoring`
3. Create `@aisdlc/skill-test-generation`

---

## Benefits

### For Teams

✅ **Modularity**: Pick only what you need
✅ **Experimentation**: Easy to A/B test TDD vs BDD
✅ **Evolution**: Change Code stage without affecting other stages
✅ **Autonomy**: Teams control their own methodology
✅ **Gradual Adoption**: Start with 1 stage, add more later

### For the Project

✅ **Decoupling**: Stages evolve independently
✅ **Marketplace Growth**: Community can contribute new variants
✅ **Clearer Dependencies**: Explicit plugin dependencies
✅ **Better Testing**: Each plugin tested in isolation

---

## Next Steps

1. **Review this proposal** with stakeholders
2. **Create prototype** of `@aisdlc/sdlc-core` + `@aisdlc/code-tdd-classic`
3. **Test plugin composition** with example team configs
4. **Migrate existing plugins** to modular architecture
5. **Document plugin development guide**
6. **Build Skills system** for reusable capabilities

---

## Questions for Discussion

1. **Backward Compatibility**: Should v3.0.0 support v2.0.0 monolithic plugin as deprecated?
2. **Default Composition**: What's the "default" plugin bundle for teams starting out?
3. **Plugin Discovery**: How do teams discover available Code stage variants?
4. **Versioning**: How do we version plugin dependencies (e.g., `code-tdd-classic@1.0.0`)?
5. **Skills Marketplace**: Should Skills be separate from Plugins, or bundled?

---

**"Excellence or nothing"** 🔥
