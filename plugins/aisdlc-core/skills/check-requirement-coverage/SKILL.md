---
name: check-requirement-coverage
description: Homeostatic sensor detecting requirements without implementation or test coverage. Scans for REQ-* keys in requirements docs and checks if they have corresponding code and tests. Use to find coverage gaps.
allowed-tools: [Read, Grep, Glob]
---

# check-requirement-coverage

**Skill Type**: Sensor (Homeostasis)
**Purpose**: Detect requirements without implementation or test coverage
**Prerequisites**: Requirements exist in documentation

---

## Agent Instructions

You are a **Sensor** in the homeostasis system. Your job is to **detect deviations** from the desired state.

**Desired State**: `coverage = 100%` (all requirements have code + tests)

Your goal is to **find requirements without coverage** and signal the deviation.

---

## Workflow

### Step 1: Find All Requirements

**Search for REQ-* keys** in requirements documentation:

```bash
# Find all requirement files
find docs/requirements -name "*.md" -type f

# Extract all REQ-* keys
grep -rho "REQ-[A-Z-]*-[0-9]*" docs/requirements/ | sort -u
```

**Example output**:
```
REQ-F-AUTH-001
REQ-F-AUTH-002
REQ-F-AUTH-003
REQ-F-PAY-001
REQ-NFR-PERF-001
REQ-NFR-SEC-001
REQ-DATA-PII-001
```

---

### Step 2: Check Implementation Coverage

**For each REQ-*, search for implementation**:

```bash
# Check if requirement has code implementation
grep -rn "# Implements: REQ-F-AUTH-001" src/

# Expected: At least 1 file with "# Implements: REQ-F-AUTH-001"
```

**Coverage criteria**:
- ✅ **Covered**: At least 1 file in `src/` has `# Implements: {REQ-KEY}`
- ❌ **Not covered**: Zero files reference the requirement

**Example**:
```
REQ-F-AUTH-001:
  ✅ src/auth/login.py:23  # Implements: REQ-F-AUTH-001
  ✅ src/auth/validators.py:67  # Implements: REQ-F-AUTH-001, BR-001
  Result: COVERED (2 files)

REQ-F-PROFILE-001:
  ❌ No files found
  Result: NOT COVERED (implementation missing)
```

---

### Step 3: Check Test Coverage

**For each REQ-*, search for tests**:

```bash
# Check if requirement has tests
grep -rn "# Validates: REQ-F-AUTH-001" tests/

# Also check BDD scenarios
grep -rn "# Validates: REQ-F-AUTH-001" features/

# Expected: At least 1 test file
```

**Coverage criteria**:
- ✅ **Covered**: At least 1 file in `tests/` or `features/` has `# Validates: {REQ-KEY}`
- ❌ **Not covered**: Zero test files reference the requirement

**Example**:
```
REQ-F-AUTH-001:
  ✅ tests/auth/test_login.py:15  # Validates: REQ-F-AUTH-001
  ✅ features/authentication.feature:8  # Validates: REQ-F-AUTH-001
  Result: COVERED (2 test files)

REQ-F-PAY-001:
  ✅ src/payments/payment.py:45  # Implements: REQ-F-PAY-001
  ❌ No test files found
  Result: COVERED (code) but NOT COVERED (tests) ⚠️
```

---

### Step 4: Calculate Coverage Percentage

**Formula**:
```python
implementation_coverage = (requirements_with_code / total_requirements) * 100
test_coverage = (requirements_with_tests / total_requirements) * 100
full_coverage = (requirements_with_both / total_requirements) * 100
```

**Example**:
```
Total Requirements: 42

Requirements with Code: 36/42 (86%)
Requirements with Tests: 32/42 (76%)
Requirements with Both: 30/42 (71%)

Coverage Status:
  ✅ Implementation: 86% (target: 80%) PASS
  ⚠️ Test: 76% (target: 80%) FAIL
  ⚠️ Full: 71% (target: 80%) FAIL
```

---

### Step 5: Identify Coverage Gaps

**Report requirements without coverage**:

**Gap Type 1: No Implementation**:
```
Requirements Without Code (6):
├─ REQ-F-PROFILE-001 - User profile editing
├─ REQ-F-PROFILE-002 - Avatar upload
├─ REQ-F-NOTIF-001 - Email notifications
├─ REQ-F-NOTIF-002 - Push notifications
├─ REQ-NFR-PERF-002 - Database optimization
└─ REQ-DATA-LIN-001 - Data lineage tracking

Recommended Action: Implement these requirements using TDD workflow
```

**Gap Type 2: Has Code, No Tests**:
```
Requirements Without Tests (10):
├─ REQ-F-PAY-001 - Payment processing
│   Code: src/payments/payment.py:45
│   Missing: Unit tests
│
├─ REQ-F-CART-001 - Shopping cart
│   Code: src/cart/cart.py:23
│   Missing: Integration tests
│
└─ ... (8 more)

Recommended Action: Invoke 'generate-missing-tests' skill
```

**Gap Type 3: Has Tests, No Code**:
```
Requirements Without Implementation (4):
├─ REQ-F-SEARCH-001 - Product search
│   Tests: tests/search/test_search.py:15
│   Missing: Implementation (tests written first - RED phase)
│
└─ ... (3 more)

Status: ✅ This is OK (RED phase of TDD)
Action: Continue to GREEN phase
```

---

## Output Format

When you detect coverage gaps:

```
[COVERAGE SENSOR - DEVIATION DETECTED]

Requirements Scanned: 42

Coverage Summary:
  Implementation: 36/42 (86%) ✅ PASS (≥80%)
  Tests: 32/42 (76%) ❌ FAIL (target: ≥80%)
  Full Coverage: 30/42 (71%) ❌ FAIL (target: ≥80%)

Homeostasis Deviation: Test coverage below 80%

Coverage Gaps by Type:

❌ No Implementation (6 requirements):
  1. REQ-F-PROFILE-001 - User profile editing
  2. REQ-F-PROFILE-002 - Avatar upload
  3. REQ-F-NOTIF-001 - Email notifications
  4. REQ-F-NOTIF-002 - Push notifications
  5. REQ-NFR-PERF-002 - Database optimization
  6. REQ-DATA-LIN-001 - Data lineage tracking

⚠️ No Tests (10 requirements):
  1. REQ-F-PAY-001 - Payment processing
     Code: src/payments/payment.py:45
  2. REQ-F-CART-001 - Shopping cart
     Code: src/cart/cart.py:23
  ... (8 more)

✅ Tests Without Implementation (4 requirements):
  1. REQ-F-SEARCH-001 - Product search
     Tests: tests/search/test_search.py:15
     Status: RED phase (OK - TDD in progress)
  ... (3 more)

Recommended Actions:
1. Invoke 'generate-missing-tests' skill for 10 requirements without tests
2. Implement 6 requirements without code (use 'tdd-workflow')
3. Continue TDD for 4 requirements in RED phase

Homeostasis Goal: coverage >= 80%
Current State: coverage = 71%
Deviation: -9% (needs correction)
```

---

## Homeostasis Behavior

**When deviation detected**:
1. **Report**: Coverage below threshold
2. **Signal**: "Need tests for {REQ-KEYS}"
3. **Recommend**: Invoke `generate-missing-tests` actuator skill
4. **Wait**: User confirmation or auto-invoke if configured

**When homeostasis achieved**:
```
[COVERAGE SENSOR - HOMEOSTASIS ACHIEVED]

Requirements: 42
Coverage: 100% (42/42) ✅

All requirements have:
  ✅ Implementation
  ✅ Tests
  ✅ Traceability

Homeostasis Status: STABLE ✓
```

---

## Prerequisites Check

None - this sensor can run anytime.

**Recommended frequency**:
- After each feature implementation
- Before commits (via pre-commit hook)
- Daily in CI/CD pipeline
- On-demand via `/coverage-req` slash command

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/aisdlc-core"
    config:
      coverage:
        minimum_percentage: 80        # Fail if coverage < 80%
        require_implementation: true  # All REQ-* must have code
        require_tests: true           # All REQ-* must have tests
        auto_generate_missing: false  # Ask before generating tests
        exclude_patterns:
          - "REQ-DATA-*"              # Don't require tests for data reqs
```

---

## Integration with Other Skills

### TDD Workflow Integration

```python
# Before starting TDD, check coverage
result = invoke_skill("check-requirement-coverage")

if result.has_gaps:
    # Report gaps to user
    print(f"Found {result.gap_count} requirements without coverage")

# After TDD, re-check coverage
result = invoke_skill("check-requirement-coverage")
if result.coverage >= 80:
    print("Coverage target achieved ✅")
```

### Generate Missing Tests Integration

```python
# Sensor detects gaps
gaps = invoke_skill("check-requirement-coverage")

if gaps.test_coverage < 80:
    # Actuator fixes gaps
    invoke_skill("generate-missing-tests", req_keys=gaps.missing_tests)

    # Re-check (should now be at homeostasis)
    new_gaps = invoke_skill("check-requirement-coverage")
    assert new_gaps.test_coverage >= 80  # Homeostasis achieved
```

---

## Next Steps

After coverage check:
1. If gaps found → Recommend actuator skills (generate-missing-tests, tdd-workflow)
2. If homeostasis → Report success
3. If configured → Auto-invoke actuator skills

---

## Notes

**Why coverage detection?**
- **Prevents forgotten requirements**: Ensures every REQ-* gets implemented
- **Quality gate**: Don't deploy without full coverage
- **Continuous monitoring**: Coverage can degrade over time
- **Homeostasis principle**: System self-corrects when coverage drops

**Sensor characteristics**:
- **Read-only**: Never modifies files (only reads)
- **Fast**: Lightweight grep operations
- **Continuous**: Can run frequently without impact
- **Objective**: Binary decision (covered or not)

**Homeostasis Goal**:
```yaml
desired_state:
  implementation_coverage: >= 80%
  test_coverage: >= 80%
  full_coverage: >= 80%
```

**"Excellence or nothing"** 🔥
