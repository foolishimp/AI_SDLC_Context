# Modular Skills Architecture for AI SDLC

**Status**: Design Proposal
**Date**: 2025-11-20
**Version**: 3.0.0 (Breaking change from v2.0.0 monolithic)

---

## Executive Summary

Refactor the monolithic `aisdlc-methodology` plugin into **composable, homeostatic skills** that Claude autonomously orchestrates based on prerequisites and requirements dependencies.

### Design Philosophy

**Core Principle**: Skills declare prerequisites (implicit dependencies), Claude autonomously orchestrates to achieve homeostasis. No prescriptive workflow, no hardcoded stage order.

**Homeostasis Model**: Requirements dependencies + skill prerequisites → emergent behavior → self-correcting system

---

## Problems with Current Architecture (v2.0.0)

```
aisdlc-methodology v2.0.0 (MONOLITHIC)
├── All 7 stages bundled together
├── TDD hardcoded as the only code approach
├── Workflow prescriptive (Requirements → Design → Tasks → Code → Test → UAT → Runtime)
├── Cannot swap individual stages
├── Cannot experiment with variations
└── Teams must fork to customize
```

**Issues**:
- ❌ **Rigid**: Fixed workflow doesn't adapt to context
- ❌ **Inflexible**: Can't swap TDD for BDD-first
- ❌ **Coupled**: Changing Code stage requires forking entire plugin
- ❌ **No Homeostasis**: System doesn't self-correct toward desired state

---

## Proposed Architecture (v3.0.0)

### Homeostatic Skills Model

```
Skills = Sensors + Actuators + Prerequisites

Claude = Homeostasis Controller
  1. Observe (Sensors detect current state)
  2. Detect Deviation (Compare to desired state)
  3. Correct (Actuators fix deviations)
  4. Verify (Sensors check again)
  5. Loop until homeostasis achieved
```

**Key Insight**: Requirements create dependencies → Dependencies create prerequisites → Prerequisites create emergent orchestration → Homeostasis

---

## Architecture Layers

### Layer 1: Foundation (Traceability Core)

**Plugin**: `@aisdlc/aisdlc-core`

**Purpose**: REQ-* key patterns and traceability rules used by all other skills

**Skills**:
- `requirement-traceability`: Defines REQ-F-*, REQ-NFR-*, REQ-DATA-*, REQ-BR-* patterns
- `check-requirement-coverage`: Detects requirements without implementation/tests (Sensor)
- `propagate-req-keys`: Tags artifacts (code, commits, tests, logs) with REQ-* (Actuator)

**Directory Structure**:
```
@aisdlc/aisdlc-core/
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
└── README.md
```

**Example Skill**: `requirement-traceability`

```yaml
---
name: requirement-traceability
description: Manage requirement key patterns and traceability rules across all SDLC stages
allowed-tools: [Read, Write]
---

# Requirement Traceability Skill

Foundation skill providing REQ-* key patterns used throughout AI SDLC.

## Requirement Key Patterns

- **Functional**: `REQ-F-{DOMAIN}-{ID}` (e.g., REQ-F-AUTH-001)
- **Non-Functional**: `REQ-NFR-{CATEGORY}-{ID}` (e.g., REQ-NFR-PERF-001)
- **Data Quality**: `REQ-DATA-{ID}` (e.g., REQ-DATA-001)
- **Business Rules**: `REQ-BR-{ID}` (e.g., REQ-BR-001)

## Traceability Rules

1. Every requirement must have unique, immutable key
2. Keys propagate through all stages:
   - Design: Components tagged with REQ-*
   - Code: Comments and commits tagged with REQ-*
   - Tests: Test functions/scenarios tagged with REQ-*
   - Runtime: Telemetry tagged with REQ-*
3. Bidirectional traceability:
   - Forward: Intent → Requirements → Design → Code → Tests → Runtime
   - Backward: Production issue → REQ-* → Original intent

## Prerequisites

None (foundation layer)

## Used By

All other skills that need requirement traceability
```

---

### Layer 2: Requirements Skills

**Plugin**: `@aisdlc/requirements-skills`

**Purpose**: Extract and manage requirements from intent

**Skills**:
- `requirement-extraction`: Transform intent (INT-*) → requirements (REQ-*)
- `create-traceability-matrix`: Build INT-* → REQ-* mapping
- `validate-requirements`: Check requirement quality (Sensor)

**Example Skill**: `requirement-extraction`

```yaml
---
name: requirement-extraction
description: Extract structured requirements with unique REQ-* keys from raw intent
allowed-tools: [Read, Write]
---

# Requirement Extraction Skill

Transform raw intent into structured requirements.

## Prerequisites

- Raw intent document (INT-*)

## Uses Skills

- `requirement-traceability` (for REQ-* key patterns)

## Workflow

1. Parse intent document
2. Identify requirement types (Functional, NFR, Data, Business Rules)
3. Generate unique REQ-* keys using patterns from `requirement-traceability`
4. Create requirements document with acceptance criteria
5. Invoke `create-traceability-matrix` to map INT-* → REQ-*

## Output

- `requirements.md` with REQ-* keys
- `traceability-matrix.yml` mapping INT-* → REQ-*

## Example

Input (intent):
```
INT-001: Build customer self-service portal
Users should be able to login and reset passwords
```

Output (requirements):
```markdown
# Requirements for INT-001

## Functional Requirements
- **REQ-F-AUTH-001**: User login with email/password
  - Acceptance: User can authenticate with valid credentials
  - Priority: High
  - Source: INT-001

- **REQ-F-AUTH-002**: User password reset via email
  - Acceptance: User receives reset link via email
  - Priority: Medium
  - Source: INT-001

## Non-Functional Requirements
- **REQ-NFR-PERF-001**: Login response < 500ms
  - Metric: p95 latency
  - Source: INT-001
```
```

---

### Layer 3: Design Skills

**Plugin**: `@aisdlc/design-skills`

**Purpose**: Design solutions while maintaining traceability

**Skills**:
- `design-with-traceability`: Create architecture/components tagged with REQ-*
- `create-adrs`: Document architectural decisions acknowledging E(t)
- `validate-design-coverage`: Check all requirements have design (Sensor)

**Example Skill**: `design-with-traceability`

```yaml
---
name: design-with-traceability
description: Create technical design tagged with requirement keys
allowed-tools: [Read, Write]
---

# Design with Traceability Skill

Create solution architecture maintaining requirement traceability.

## Prerequisites

- Requirements (REQ-*) must exist
- Ecosystem constraints E(t) known

## Uses Skills

- `requirement-traceability` (for REQ-* tagging)
- `create-adrs` (for documenting decisions)

## Workflow

1. Read requirements from `requirements.md`
2. Design components/services for each REQ-*
3. Tag design artifacts with REQ-* keys
4. Document architectural decisions via ADRs
5. Create traceability matrix: REQ-* → Components

## Output

- Component diagrams (tagged with REQ-*)
- API specifications (tagged with REQ-*)
- Data models (tagged with REQ-*)
- ADRs (acknowledging E(t) constraints)
- Design traceability matrix

## Example

```yaml
# Component: AuthenticationService
requirements:
  - REQ-F-AUTH-001  # User login
  - REQ-F-AUTH-002  # Password reset
  - REQ-NFR-PERF-001  # Performance

api_endpoints:
  - POST /api/v1/auth/login  # REQ-F-AUTH-001
  - POST /api/v1/auth/reset  # REQ-F-AUTH-002

constraints:
  - E(t): Must use existing OAuth2 platform
  - E(t): PII regulations require encryption at rest
```
```

---

### Layer 4a: Code Skills (TDD Variant)

**Plugin**: `@aisdlc/code-tdd-skills`

**Purpose**: Implement code using TDD while maintaining traceability

**Skills**:
- `tdd-workflow`: RED → GREEN → REFACTOR → COMMIT orchestration
- `red-phase`: Write failing test tagged with REQ-*
- `green-phase`: Implement minimal code tagged with REQ-*
- `refactor-phase`: Improve code quality
- `commit-with-req-tag`: Git commit with REQ-* in message

**Example Skill**: `tdd-workflow`

```yaml
---
name: tdd-workflow
description: Test-Driven Development workflow maintaining requirement traceability
allowed-tools: [Read, Write, Edit, Bash]
---

# TDD Workflow Skill

Follow RED → GREEN → REFACTOR → COMMIT while maintaining traceability.

## Prerequisites

- Work unit with REQ-* tag (from Tasks stage or manual assignment)
- Requirement details available

## Uses Skills

- `requirement-traceability` (for REQ-* patterns)
- `red-phase` (write failing test)
- `green-phase` (make test pass)
- `refactor-phase` (improve code)
- `commit-with-req-tag` (commit with REQ-*)
- `propagate-req-keys` (tag code/tests with REQ-*)

## Workflow

### 1. RED Phase
- Invoke: `red-phase` skill
- Write failing test for REQ-*
- Ensure test fails for right reason
- Commit: "RED: Add test for {REQ-*}"

### 2. GREEN Phase
- Invoke: `green-phase` skill
- Write minimal code to pass test
- No refactoring yet
- Tag code with REQ-* in comments
- Commit: "GREEN: Implement {REQ-*}"

### 3. REFACTOR Phase
- Invoke: `refactor-phase` skill
- Improve code quality
- Keep tests passing
- Add logging tagged with REQ-*
- Commit: "REFACTOR: Clean up {REQ-*}"

### 4. COMMIT Phase
- Invoke: `commit-with-req-tag` skill
- Final commit: "feat: {description} ({REQ-*})"
- Update traceability matrix: REQ-* → [commits, tests, code files]

## Homeostasis Behavior

If prerequisites missing:
1. Detect: No REQ-* key for work unit
2. Signal: "Need requirement extraction first"
3. Claude invokes: `requirement-extraction` skill
4. Retry: `tdd-workflow` skill with new REQ-*

## Example

```python
# RED Phase
# Validates: REQ-F-AUTH-001
def test_user_login_with_valid_credentials():
    result = login("user@example.com", "password123")
    assert result.success == True

# GREEN Phase
# Implements: REQ-F-AUTH-001
def login(email: str, password: str) -> LoginResult:
    user = User.get_by_email(email)
    if user and user.check_password(password):
        return LoginResult(success=True, user=user)
    return LoginResult(success=False)

# REFACTOR Phase
def login(email: str, password: str) -> LoginResult:
    """User authentication.

    Implements: REQ-F-AUTH-001
    """
    logger.info("User login attempt", extra={
        "requirement": "REQ-F-AUTH-001",
        "email": email
    })

    user = User.get_by_email(email)
    if user and user.check_password(password):
        logger.info("Login successful", extra={"requirement": "REQ-F-AUTH-001"})
        return LoginResult(success=True, user=user)

    logger.warning("Login failed", extra={"requirement": "REQ-F-AUTH-001"})
    return LoginResult(success=False)
```
```

---

### Layer 4b: Code Skills (BDD Variant)

**Plugin**: `@aisdlc/code-bdd-skills`

**Purpose**: Implement code using BDD while maintaining traceability

**Skills**:
- `bdd-workflow`: SCENARIO → STEP DEF → IMPLEMENT → REFACTOR
- `write-scenario`: Create Gherkin scenario tagged with REQ-*
- `implement-step-definitions`: Write step definitions
- `implement-feature`: Make scenarios pass
- `refactor-bdd`: Clean up scenarios and code

**Example Skill**: `write-scenario`

```yaml
---
name: write-scenario
description: Create BDD scenario in Gherkin format tagged with requirement key
allowed-tools: [Write]
---

# Write Scenario Skill

Create Gherkin scenario for requirement.

## Prerequisites

- Requirement (REQ-*) must exist

## Uses Skills

- `requirement-traceability` (for REQ-* tagging)

## Workflow

1. Read requirement details
2. Write Feature file with REQ-* tag
3. Create Given/When/Then scenario in business language
4. Tag scenario with REQ-* key

## Output

Feature file (`.feature`) tagged with REQ-*

## Example

```gherkin
# Validates: REQ-F-AUTH-001
Feature: User Authentication

  As a customer
  I want to login with email and password
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I am on the login page
    And I have a valid account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter password "password123"
    And I click the "Login" button
    Then I should see "Welcome back"
    And I should be redirected to the dashboard
```
```

---

### Layer 5: Testing Skills

**Plugin**: `@aisdlc/testing-skills`

**Purpose**: Validate test coverage and generate missing tests

**Skills**:
- `validate-test-coverage`: Check REQ-* → test mapping (Sensor)
- `generate-missing-tests`: Create tests for uncovered requirements (Actuator)
- `run-integration-tests`: Execute tests tagged with REQ-*
- `create-coverage-report`: Generate REQ-* coverage matrix (Sensor)

**Example Skill**: `validate-test-coverage`

```yaml
---
name: validate-test-coverage
description: Detect requirements without sufficient test coverage (Homeostasis Sensor)
allowed-tools: [Read, Bash]
---

# Validate Test Coverage Skill

Homeostasis sensor detecting coverage deviations.

## Prerequisites

- Requirements (REQ-*) exist
- Code exists

## Uses Skills

- `check-requirement-coverage` (from aisdlc-core)

## Workflow

1. Scan traceability matrix for REQ-* → test mapping
2. Run test coverage tools (pytest, coverage.py)
3. Detect deviations:
   - REQ-* with 0% test coverage
   - REQ-* with < 80% test coverage
   - REQ-* with no tests at all
4. Signal deviations to Claude

## Output

Coverage deviation report:
```yaml
coverage_deviations:
  - requirement: REQ-F-AUTH-001
    coverage: 100%
    status: OK ✓

  - requirement: REQ-F-AUTH-002
    coverage: 0%
    status: DEVIATION ✗
    action: Generate tests

  - requirement: REQ-NFR-PERF-001
    coverage: 50%
    status: DEVIATION ✗
    action: Add performance tests
```

## Homeostasis Behavior

When deviations detected:
1. Signal to Claude: "Coverage gaps found"
2. Claude invokes: `generate-missing-tests` skill (Actuator)
3. Tests generated for missing REQ-*
4. Claude re-invokes: `validate-test-coverage` skill (Sensor)
5. Loop until all requirements >= 80% coverage
```

---

### Layer 6: Runtime Skills

**Plugin**: `@aisdlc/runtime-skills`

**Purpose**: Runtime telemetry and feedback loop

**Skills**:
- `telemetry-tagging`: Tag logs/metrics/alerts with REQ-*
- `create-observability-config`: Setup Datadog/Splunk with REQ-* tags
- `trace-production-issue`: Alert → REQ-* → Intent (Sensor)

**Example Skill**: `trace-production-issue`

```yaml
---
name: trace-production-issue
description: Trace production alert back to requirement and create new intent (Feedback Loop Sensor)
allowed-tools: [Read, Write]
---

# Trace Production Issue Skill

Close the feedback loop: Production → REQ-* → Intent

## Prerequisites

- Production alert/issue detected
- Alert tagged with REQ-* key

## Uses Skills

- `requirement-traceability` (to trace REQ-* → INT-*)

## Workflow

1. Parse production alert for REQ-* tag:
   ```
   Alert: "ERROR: REQ-F-AUTH-001 - Auth timeout after 5s"
   ```

2. Trace back to original intent:
   ```yaml
   REQ-F-AUTH-001 → INT-001 (Customer self-service portal)
   ```

3. Create new intent:
   ```
   INT-042: Fix auth timeout
   Related: REQ-F-AUTH-001, INT-001
   Impact: Users cannot login (production down)
   Priority: P0
   ```

4. Trigger new SDLC cycle:
   - INT-042 → New requirements (REQ-F-AUTH-003: "Timeout handling")
   - Homeostasis loop begins again

## Output

- New intent (INT-*) created
- Traceability maintained: Production issue → REQ-* → Original intent
- Feedback loop closed ✓

## Example

```
Production Alert (Datadog):
  Name: "Auth Timeout"
  Message: "ERROR: REQ-F-AUTH-001 - Database connection timeout"
  Tags: ["requirement:REQ-F-AUTH-001", "severity:critical"]

↓ Trace back

Requirement:
  REQ-F-AUTH-001: User login with email/password
  Source: INT-001

↓ Create new intent

New Intent:
  INT-042: Fix database timeout in authentication
  Related: REQ-F-AUTH-001, INT-001
  Impact: 100% of login attempts failing
  Priority: P0

↓ Homeostasis loop restarts

Requirements Agent extracts:
  REQ-F-AUTH-003: Handle database timeouts gracefully
  REQ-NFR-PERF-002: Retry logic with exponential backoff
```
```

---

### Layer 7: Principle Packs

**Plugin**: `@aisdlc/principles-key`

**Purpose**: Apply Key Principles during development

**Skills**:
- `apply-key-principles`: Enforce TDD, Fail Fast, Modular, etc.
- `seven-questions-checklist`: Validate before coding (Sensor)

**Example Skill**: `seven-questions-checklist`

```yaml
---
name: seven-questions-checklist
description: Ask seven questions before coding (Key Principles validator)
allowed-tools: []
---

# Seven Questions Checklist Skill

Homeostasis sensor enforcing Key Principles.

## Prerequisites

- About to write production code

## Workflow

Ask these seven questions:

1. **Tests First?** (Principle #1: TDD)
   - Have I written tests first?
   - If NO → Invoke `red-phase` skill

2. **Fail Loud?** (Principle #2: Fail Fast & Root Cause)
   - Will this fail loudly if wrong?
   - If NO → Add assertions and error handling

3. **Module Focused?** (Principle #3: Modular & Maintainable)
   - Is this module single-responsibility?
   - If NO → Refactor into smaller modules

4. **Check if Exists?** (Principle #4: Reuse Before Build)
   - Did I search for existing solutions?
   - If NO → Search codebase/libraries first

5. **Researched Alternatives?** (Principle #5: Open Source First)
   - Have I researched open-source options?
   - If NO → Suggest alternatives to user

6. **Avoiding Tech Debt?** (Principle #6: No Legacy Baggage)
   - Am I introducing technical debt?
   - If YES → Rethink approach

7. **Is This Excellent?** (Principle #7: Perfectionist Excellence)
   - Is this best-of-breed quality?
   - If NO → Improve until excellent

## Output

```
Seven Questions Checklist:
  1. Tests first? ✓
  2. Fail loud? ✓
  3. Module focused? ✗ → Refactor needed
  4. Check if exists? ✓
  5. Researched alternatives? ✓
  6. Avoiding tech debt? ✓
  7. Is this excellent? ✗ → Improve quality

Action: Do not proceed with coding yet
```

## Homeostasis Behavior

If any question = NO:
1. Signal deviation to Claude
2. Claude invokes corrective skill
3. Re-check questions
4. Loop until all = YES
```

---

## Homeostasis Flow Example

### Scenario: User Says "Implement authentication feature"

**Installed Plugins**:
```yaml
- @aisdlc/aisdlc-core
- @aisdlc/requirements-skills
- @aisdlc/code-tdd-skills
- @aisdlc/testing-skills
- @aisdlc/principles-key
```

**Claude's Autonomous Orchestration**:

```
Step 1: Observe Context
  - User intent: "authentication feature"
  - No REQ-* keys exist in project
  - Sensor: check-requirement-coverage detects no requirements

Step 2: Detect Deviation
  - Expected: Requirements exist
  - Actual: No requirements
  - Deviation: Cannot implement without requirements

Step 3: Correct Deviation
  - Invoke: requirement-extraction skill
  - Prerequisites: Intent exists ✓
  - Output: REQ-F-AUTH-001, REQ-NFR-PERF-001, REQ-DATA-001
  - Invoke: create-traceability-matrix skill
  - Output: INT-001 → [REQ-F-AUTH-001, ...]

Step 4: Validate Principles
  - Invoke: seven-questions-checklist skill
  - Question 1: "Tests first?" → YES (will use TDD)
  - Question 4: "Check if exists?" → Search for auth code
  - All questions: YES ✓

Step 5: Implement with TDD
  - Invoke: tdd-workflow skill
  - Prerequisites check:
    - Work unit with REQ-* tag? ✓ (REQ-F-AUTH-001)
    - Requirement details available? ✓
  - Invoke: red-phase skill
    - Output: test_user_login() tagged with REQ-F-AUTH-001
  - Invoke: green-phase skill
    - Output: login() implementation tagged with REQ-F-AUTH-001
  - Invoke: refactor-phase skill
    - Output: Improved code with logging (tagged with REQ-*)
  - Invoke: commit-with-req-tag skill
    - Output: "feat: Add user login (REQ-F-AUTH-001)"

Step 6: Validate Coverage (Homeostasis Check)
  - Invoke: validate-test-coverage skill
  - Sensor detects:
    - REQ-F-AUTH-001: 100% coverage ✓
    - REQ-NFR-PERF-001: 0% coverage ✗ (no performance test)
    - REQ-DATA-001: 50% coverage ✗ (partial validation)
  - Deviation detected!

Step 7: Correct Coverage Gaps
  - Invoke: generate-missing-tests skill (Actuator)
  - Prerequisites: Coverage gaps identified ✓
  - Uses: tdd-workflow skill to create tests
  - Output:
    - test_login_performance() for REQ-NFR-PERF-001
    - test_email_validation() for REQ-DATA-001

Step 8: Validate Again
  - Invoke: validate-test-coverage skill
  - Sensor detects:
    - REQ-F-AUTH-001: 100% coverage ✓
    - REQ-NFR-PERF-001: 100% coverage ✓
    - REQ-DATA-001: 100% coverage ✓
  - No deviations!
  - Homeostasis achieved ✓

Step 9: Final Verification
  - All requirements have tests ✓
  - All tests passing ✓
  - Code tagged with REQ-* ✓
  - Commits tagged with REQ-* ✓
  - Traceability matrix updated ✓
```

**Key Point**: No prescribed workflow. Claude orchestrated based on:
- Skill prerequisites (implicit dependencies)
- Deviation detection (sensors)
- Corrective actions (actuators)
- Homeostasis goal (100% coverage)

---

## Team Composition Examples

### Startup Team (Minimal)

```yaml
# .claude/plugins.yml
plugins:
  - "@aisdlc/aisdlc-core"        # Traceability foundation
  - "@aisdlc/code-tdd-skills"    # TDD workflow
```

**Behavior**:
- Code and commits tagged with REQ-*
- TDD workflow enforced
- Minimal overhead
- No formal requirements stage (REQ-* created ad-hoc)

**Homeostasis**:
- Sensor: check-requirement-coverage detects missing REQ-*
- Actuator: tdd-workflow creates REQ-* on-the-fly
- Self-corrects toward traceability

---

### Enterprise Team (Full Stack)

```yaml
# .claude/plugins.yml
plugins:
  - "@aisdlc/aisdlc-core"              # Traceability foundation
  - "@aisdlc/requirements-skills"      # Formal requirements extraction
  - "@aisdlc/design-skills"            # Design with ADRs
  - "@aisdlc/code-tdd-skills"          # TDD workflow
  - "@aisdlc/testing-skills"           # Coverage validation
  - "@aisdlc/runtime-skills"           # Telemetry + feedback loop
  - "@aisdlc/principles-key"           # Key Principles enforcement
```

**Behavior**:
- Full 7-stage SDLC (emergent, not prescribed)
- Complete bidirectional traceability
- ADRs acknowledging E(t)
- Seven questions checklist
- Production feedback loop

**Homeostasis**:
- Multiple sensors: coverage, principles, design
- Multiple actuators: requirements, code, tests, telemetry
- Self-corrects toward 100% coverage, quality, traceability

---

### Experimental Team (BDD-First)

```yaml
# .claude/plugins.yml
plugins:
  - "@aisdlc/aisdlc-core"              # Traceability foundation
  - "@aisdlc/requirements-skills"      # Requirements extraction
  - "@aisdlc/code-bdd-skills"          # BDD workflow (not TDD!)
  - "@aisdlc/testing-skills"           # Coverage validation
```

**Behavior**:
- BDD scenarios before code
- Gherkin tagged with REQ-*
- Step definitions → implementation
- Coverage validation

**Homeostasis**:
- Sensor: validate-test-coverage checks scenario coverage
- Actuator: bdd-workflow creates scenarios for missing REQ-*
- Self-corrects toward complete scenario coverage

---

## Key Benefits

### For Teams

✅ **Modularity**: Install only needed skills
✅ **Experimentation**: Swap TDD for BDD without breaking
✅ **Evolution**: Add skills as team matures
✅ **Autonomy**: Claude orchestrates, not rigid workflow
✅ **Homeostasis**: System self-corrects toward desired state

### For the Methodology

✅ **Emergent Behavior**: Workflow emerges from prerequisites
✅ **Self-Correcting**: Sensors detect deviations, actuators fix
✅ **Traceability-First**: REQ-* keys are foundational
✅ **Adaptive**: Works for startup or enterprise
✅ **No Prescription**: No hardcoded "Stage 1 → Stage 2"

---

## Migration Path from v2.0.0 → v3.0.0

### Phase 1: Create Core (Week 1)
1. Extract `@aisdlc/aisdlc-core` from v2.0.0
2. Create foundation skills:
   - requirement-traceability
   - check-requirement-coverage
   - propagate-req-keys

### Phase 2: Requirements Skills (Week 2)
1. Create `@aisdlc/requirements-skills`
2. Extract skills:
   - requirement-extraction
   - create-traceability-matrix
   - validate-requirements

### Phase 3: Code Skills (Week 3-4)
1. Create `@aisdlc/code-tdd-skills`
2. Extract TDD workflow skills
3. Create `@aisdlc/code-bdd-skills`
4. Implement BDD workflow skills

### Phase 4: Testing & Runtime (Week 5)
1. Create `@aisdlc/testing-skills`
2. Create `@aisdlc/runtime-skills`
3. Implement homeostasis sensors/actuators

### Phase 5: Principles (Week 6)
1. Create `@aisdlc/principles-key`
2. Extract Key Principles skills
3. Implement seven-questions-checklist

### Phase 6: Testing & Documentation (Week 7-8)
1. Test team compositions
2. Verify homeostasis behavior
3. Document skill prerequisites
4. Create migration guide

---

## Questions for Discussion

1. **Skill Granularity**: Should `tdd-workflow` be one skill or separate `red-phase`, `green-phase`, etc.?
   - **Recommendation**: Both - `tdd-workflow` orchestrates individual phase skills

2. **Prerequisite Validation**: Should skills fail loudly if prerequisites missing?
   - **Recommendation**: Signal to Claude, let Claude invoke missing skills

3. **Homeostasis Convergence**: How many iterations before giving up?
   - **Recommendation**: Configurable max iterations (default: 5)

4. **Sensor Frequency**: How often do sensors check for deviations?
   - **Recommendation**: After each actuator completes

5. **Skill Discovery**: How do teams find available skills?
   - **Recommendation**: `/skills` command shows all installed skills

---

## Next Steps

1. ✅ Review this design with stakeholders
2. Create `@aisdlc/aisdlc-core` plugin with foundation skills
3. Extract `@aisdlc/code-tdd-skills` as proof-of-concept
4. Test homeostasis with 2-3 team compositions
5. Iterate based on feedback
6. Complete remaining skill plugins
7. Document skill development guide
8. Publish to marketplace

---

**"Excellence or nothing"** 🔥
