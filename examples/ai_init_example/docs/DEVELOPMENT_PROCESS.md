# TDD Development Process - 7 Steps

This document describes the traditional Test-Driven Development process.

## The 7 Steps

### Phase 1: Preparation
**Step 1: UNDERSTAND** - Understand the requirement
- Read user story
- Clarify acceptance criteria
- Identify edge cases
- Document assumptions

### Phase 2: Test-Driven Development
**Step 2: RED** - Write failing test
- Write test first
- Test should fail (red)
- Verify test quality
- Run test suite

**Step 3: GREEN** - Write minimal code
- Implement just enough code
- Make the test pass (green)
- Don't optimize yet
- Run all tests

**Step 4: REFACTOR** - Improve code quality
- Enhance design
- Remove duplication
- Improve readability
- Keep tests green

### Phase 3: Validation
**Step 5: TEST** - Run full test suite
- Unit tests
- Integration tests
- Regression tests
- Check coverage

**Step 6: COMMIT** - Commit with message
- Stage changes
- Write descriptive commit message
- Include test info
- Push to remote

**Step 7: DEPLOY** - Deploy to environment
- Deploy to dev/staging/prod
- Verify deployment
- Monitor for issues
- Update documentation

## Quick Workflow

```
UNDERSTAND → RED → GREEN → REFACTOR → TEST → COMMIT → DEPLOY
    ↓        ↓      ↓        ↓          ↓       ↓        ↓
Clarify → Fail → Pass → Clean → Verify → Save → Release
```

## Example

### Step 1: UNDERSTAND
```
User Story: As a developer, I want to load config from YAML
Acceptance: Config loads successfully from file path
```

### Step 2: RED
```python
def test_load_config():
    config = load_config("test.yml")
    assert config is not None
    # Test fails - function doesn't exist yet
```

### Step 3: GREEN
```python
def load_config(path):
    return {}  # Minimal implementation
```

### Step 4: REFACTOR
```python
def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)
```

### Steps 5-7: Validation & Deployment
- Run full test suite
- Commit with message
- Deploy to environment

---

This process ensures code quality through systematic testing.
