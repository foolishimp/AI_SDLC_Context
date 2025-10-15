# Session Starter - AI Init with AI_SDLC_Context

## Starting a Development Session

### 1. Check Current State
```bash
git status
git pull origin main
```

### 2. Load Configuration
```python
from ai_sdlc_config import ConfigManager

manager = ConfigManager()
manager.load_hierarchy("configs/base.yml")
manager.load_hierarchy("configs/development.yml")
manager.merge()
```

### 3. Review Active Tasks
```bash
cat claude_tasks/active/ACTIVE_TASKS.md
```

### 4. Check Principles
- Test Driven Development
- Fail Fast & Root Cause
- Modular & Maintainable
- Reuse Before Build
- Open Source First
- No Legacy Baggage
- Perfectionist Excellence

### 5. Run Tests
```bash
pytest
# Ensure clean state before starting
```

### 6. Choose Workflow

**BDD (9 steps):** SPECIFY → COLLABORATE → RED → GREEN → REFACTOR → VALIDATE → DOCUMENT → DEMO → ITERATE

**TDD (7 steps):** UNDERSTAND → RED → GREEN → REFACTOR → TEST → COMMIT → DEPLOY

### 7. Start Work
- Create feature branch (optional)
- Write scenario/test first
- Implement code
- Commit frequently

---

Ready to develop!
