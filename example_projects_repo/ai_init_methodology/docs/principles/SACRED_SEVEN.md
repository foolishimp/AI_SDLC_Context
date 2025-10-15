# 🎯 The Sacred Seven Principles

## Core Development Methodology for AI_SDLC_Context

These seven principles form the foundation of all development in this project. They are adapted from the [ai_init](https://github.com/foolishimp/ai_init) project and represent our unwavering commitment to excellence.

---

## The Sacred Seven

### 1️⃣ Test Driven Development
**"No code without tests"**

- **Workflow**: RED → GREEN → REFACTOR
- Write tests first, always
- Maintain >80% code coverage
- Tests are documentation

**In Practice**:
```python
# ❌ Wrong: Write code first
def merge_hierarchies(hierarchies):
    # implementation...

# ✅ Right: Write test first
def test_merge_hierarchies():
    assert merger.merge([base, override]) == expected

# Then write implementation
def merge_hierarchies(hierarchies):
    # implementation...
```

---

### 2️⃣ Fail Fast & Root Cause
**"Break loudly, fix completely"**

- No workarounds or band-aids
- Fix the cause, not symptoms
- Let errors be obvious
- No hiding bugs

**In Practice**:
```python
# ❌ Wrong: Silence errors
try:
    load_config(path)
except:
    pass  # Hide the problem

# ✅ Right: Fail loudly
def load_config(path):
    if not Path(path).exists():
        raise FileNotFoundError(f"Config not found: {path}")
```

---

### 3️⃣ Modular & Maintainable
**"Single responsibility, loose coupling"**

- Each module does one thing well
- Decoupled components
- Easy to understand
- Easy to extend

**In Practice**:
```python
# ❌ Wrong: God class doing everything
class ConfigSystem:
    def load_yaml(self): ...
    def merge_configs(self): ...
    def resolve_uris(self): ...
    def query_llm(self): ...

# ✅ Right: Focused classes
class YAMLLoader:
    def load(self, path): ...

class HierarchyMerger:
    def merge(self, hierarchies): ...

class URIResolver:
    def resolve(self, uri_ref): ...
```

---

### 4️⃣ Reuse Before Build
**"Check first, create second"**

- Search existing code before writing new
- Use what exists
- Document new creations
- Avoid duplication

**In Practice**:
```python
# Before writing new code, ask:
# 1. Does this functionality exist?
# 2. Can I reuse an existing pattern?
# 3. Is there a library for this?

# ✅ Right: Reuse existing
from pathlib import Path  # Don't write your own path handling
import yaml  # Don't write your own YAML parser
```

---

### 5️⃣ Open Source First
**"Suggest alternatives, human decides"**

- Research existing libraries
- Claude suggests options
- Human makes final choice
- Prefer battle-tested solutions

**In Practice**:
```markdown
When needing URI parsing:
- Option 1: urllib.parse (built-in)
- Option 2: requests (popular)
- Option 3: httpx (modern)

Recommendation: Use urllib.parse for basic needs,
httpx for advanced features. Human decides.
```

---

### 6️⃣ No Legacy Baggage
**"Clean slate, no debt"**

- No backwards compatibility constraints
- No technical debt
- Replace completely if needed
- Fresh start mentality

**In Practice**:
```python
# ✅ Right: Clean breaks
# v1.0 → v2.0 with breaking changes is OK
# Document migration path clearly
# Don't carry old cruft forward

# If HierarchyNode design is flawed:
# - Design HierarchyNode v2
# - Provide migration tools
# - Don't patch the old design
```

---

### 7️⃣ Perfectionist Excellence
**"Best of breed only"**

- Quality over quantity
- Ship when excellent, not "good enough"
- Hardcore standards
- No compromises on quality

**Ultimate Mantra**: **"Excellence or nothing"**

**In Practice**:
```python
# ❌ Wrong: Ship it, we'll fix later
def merge(hierarchies):
    # TODO: Handle edge cases
    # TODO: Improve performance
    # TODO: Add validation
    return quick_dirty_merge(hierarchies)

# ✅ Right: Ship it right
def merge(self, hierarchies: List[HierarchyNode]) -> HierarchyNode:
    """
    Merge multiple hierarchies with priority-based overrides.

    Fully tested, documented, and handles all edge cases.
    """
    if not hierarchies:
        raise ValueError("Cannot merge empty list")
    # Complete, correct implementation
```

---

## 🚀 Quick Decision Tree

```
Need to build something?
│
├─ #4: Does it exist already? → Use existing
│
├─ #5: Is there an open source solution? → Evaluate options
│
├─ #1: Write tests first → RED phase
│
├─ #2: Let it fail visibly → No silent errors
│
├─ #3: Make it modular → Single responsibility
│
├─ #6: Don't carry debt → Clean implementation
│
└─ #7: Make it excellent → Ship quality
```

---

## 🔥 The Mantras

1. **"Tests before code"** - Principle #1
2. **"Fail loud, fix deep"** - Principle #2
3. **"One job per module"** - Principle #3
4. **"Search before create"** - Principle #4
5. **"Suggest, don't decide"** - Principle #5
6. **"No debt, fresh start"** - Principle #6
7. **"Excellence or nothing"** - Principle #7

---

## Application to AI_SDLC_Context

### Our Commitment

Every component in this project adheres to the Sacred Seven:

#### Models (`src/ai_sdlc_config/models/`)
- ✅ Comprehensive unit tests (51 tests)
- ✅ Single responsibility (HierarchyNode, URIReference)
- ✅ Clean, modular design

#### Loaders (`src/ai_sdlc_config/loaders/`)
- ✅ Test-driven (28 tests for YAML, 28 for URI)
- ✅ Reuses standard libraries (yaml, urllib)
- ✅ Fails fast with clear errors

#### Mergers (`src/ai_sdlc_config/mergers/`)
- ✅ Well-tested (31 tests)
- ✅ Clean merge strategies
- ✅ No hidden complexity

#### Core API (`src/ai_sdlc_config/core/`)
- ✅ Integration tested (18 tests)
- ✅ High-level, easy to use
- ✅ Excellent documentation

**Total**: 156 tests, 100% passing, comprehensive coverage

---

## Before You Code

Ask yourself:

1. **Have I written tests first?** (Principle #1)
2. **Will this fail loudly if something's wrong?** (Principle #2)
3. **Does this module have a single, clear purpose?** (Principle #3)
4. **Did I check if this already exists?** (Principle #4)
5. **Have I researched alternatives?** (Principle #5)
6. **Am I avoiding technical debt?** (Principle #6)
7. **Is this the best possible implementation?** (Principle #7)

If you can't answer "yes" to all seven, **don't write the code yet**.

---

## Violations Are Unacceptable

The Sacred Seven are not guidelines - they are **requirements**.

- Code without tests → **Rejected**
- Silent error handling → **Rejected**
- God classes → **Rejected**
- Duplicated functionality → **Rejected**
- Undocumented library choices → **Rejected**
- Technical debt → **Rejected**
- "Good enough" quality → **Rejected**

---

## References

- **Origin**: [ai_init project](https://github.com/foolishimp/ai_init)
- **Applied In**: All AI_SDLC_Context development
- **Enforcement**: Code reviews, CI/CD, peer accountability

---

*These principles are the foundation of our excellence. They are not negotiable.*

**Excellence or nothing. 🔥**
