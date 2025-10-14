# Development Principles Quick Card

## The 7 Core Principles

### 1. Test Driven Development
**Behaviors before tests before code**
- Write Gherkin scenarios first
- Then write failing tests
- Then write code to pass
- No code without tests

### 2. Fail Fast & Root Cause
**Fix problems at source**
- Don't work around issues
- Find and fix root cause
- Fail early in pipeline
- Log errors clearly

### 3. Modular & Maintainable
**Single responsibility**
- One function, one purpose
- Loose coupling
- High cohesion
- Easy to test

### 4. Reuse Before Build
**Check existing code first**
- Search codebase
- Check standard library
- Review open source
- Only build if necessary

### 5. Open Source First
**Suggest alternatives**
- Prefer established libraries
- Contribute back
- Follow community standards
- Build on shoulders of giants

### 6. No Legacy Baggage
**Clean slate approach**
- Don't inherit technical debt
- Start fresh when possible
- Modernize dependencies
- Remove unused code

### 7. Perfectionist Excellence
**Best of breed only**
- High quality standards
- Complete testing
- Clear documentation
- Production ready

## BDD Principles

### Behavior-First
Start with business outcomes, not technical implementation

### Stakeholder Collaboration
Include business in specification process

### Living Documentation
Scenarios become documentation that stays current

### Outside-In Development
Work from user value to implementation

## Quick Checklist

Before committing:
- [ ] Scenarios written and passing
- [ ] Tests written and passing
- [ ] Code follows single responsibility
- [ ] Checked for existing solutions
- [ ] No workarounds or technical debt
- [ ] High quality, production-ready
- [ ] Documentation updated
- [ ] Coverage > 80%

## Configuration Access

With AI_SDLC_config:

```python
# Get all principles
principles = manager.find_all("principles.*")

# Get specific principle
for path, node in principles:
    name = node.get_value_by_path("name")
    desc = node.get_value_by_path("description")
    priority = node.get_value_by_path("priority")
    print(f"{priority}. {name}: {desc}")
```

## Integration with Workflow

1. **SPECIFY** - Define behavior (Principle #1)
2. **RED** - Write failing test (Principle #1)
3. **GREEN** - Minimal code (Principle #3, #6)
4. **REFACTOR** - Check reuse (Principle #4, #5)
5. **VALIDATE** - High quality (Principle #7)
6. **ITERATE** - Fix at source (Principle #2)

---

*Keep this card handy during development*
