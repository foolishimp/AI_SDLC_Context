# Quick Reference - AI Init with AI_SDLC_config

## Installation

```bash
# Download installer
curl -O https://raw.githubusercontent.com/foolishimp/claude_init/main/setup_claude_tasks.py

# Run with AI_SDLC_config
python setup_claude_tasks.py --config ai_init_config.yml

# Clean up
rm setup_claude_tasks.py
```

## Configuration Loading

```python
from ai_sdlc_config import ConfigManager

# Load configuration layers
manager = ConfigManager(base_path="configs")
manager.load_hierarchy("base.yml")           # Base config
manager.load_hierarchy("development.yml")    # Environment
manager.add_runtime_overrides({              # Runtime
    "setup.force_overwrite": True
})
manager.merge()

# Access values
principles = manager.find_all("principles.*")
bdd_process = manager.get_content("methodology.bdd_process")
```

## BDD+TDD Workflow

### Quick Commands
```bash
# 1. Start new feature
vim claude_tasks/behaviors/features/my_feature.feature

# 2. Run BDD scenarios
pytest claude_tasks/behaviors/

# 3. Generate report
pytest --html=claude_tasks/behaviors/reports/report.html

# 4. Check tasks
cat claude_tasks/active/ACTIVE_TASKS.md
```

### 9-Step Process
```
1. SPECIFY     - Write Gherkin scenarios
2. COLLABORATE - Review with stakeholders
3. RED         - Write failing tests
4. GREEN       - Make tests pass
5. REFACTOR    - Clean up code
6. VALIDATE    - Run scenarios
7. DOCUMENT    - Generate reports
8. DEMO        - Show stakeholders
9. ITERATE     - Incorporate feedback
```

## Configuration Structure

### Methodology Files (URI References)
```yaml
methodology:
  bdd_process: "file://docs/BDD_PROCESS.md"
  tdd_workflow: "file://docs/DEVELOPMENT_PROCESS.md"
  quick_reference: "file://docs/QUICK_REFERENCE.md"
```

### Principles (Dot Hierarchy)
```yaml
principles:
  test_driven:
    name: "Test Driven Development"
    priority: 1
  fail_fast:
    name: "Fail Fast & Root Cause"
    priority: 2
  # ... 7 total principles
```

### Access in Code
```python
# Get all principles
principles = manager.find_all("principles.*")

# Get specific principle
tdd = manager.get_value("principles.test_driven.description")

# Get referenced document
bdd_doc = manager.get_content("methodology.bdd_process")
```

## Task Management

### Create Task
```markdown
### Task 1: New Feature
- **Priority**: High
- **Status**: Not Started
- **Behavior**: See `features/new_feature.feature`
- **Acceptance Criteria**:
  - [ ] Scenario passes
  - [ ] Tests green
  - [ ] Documentation updated
```

### Complete Task
```bash
# Move to finished
mv task.md claude_tasks/finished/$(date +%Y%m%d_%H%M)_feature_name.md

# Commit
git commit -m "Task #1: Implement new feature

Added feature with BDD scenarios.

Tests: 5 unit | Coverage: 95%
BDD: SPECIFY → RED → GREEN → REFACTOR → VALIDATE"
```

## Git Workflow

### With Config Template
```python
# Get commit template
template = manager.get_value("git.commit_template")

# Format with values
message = template.format(
    task_number=1,
    task_title="New Feature",
    description="Implemented with BDD",
    test_count=5,
    coverage=95,
    workflow="BDD",
    steps="SPECIFY → RED → GREEN → REFACTOR → VALIDATE"
)
```

### Commit
```bash
git add .
git commit -m "$message"
```

## URLs and Resources

```python
# Get URLs from config
github = manager.get_value("urls.github")
installer = manager.get_value("urls.installer_raw")

print(f"Repo: {github}")
print(f"Installer: {installer}")
```

## Environment-Specific Behavior

### Development
```python
manager.load_hierarchy("development.yml")
# Gets: debug_mode=true, verbose=true, auto_start=true
```

### Production
```python
manager.load_hierarchy("production.yml")
# Gets: debug_mode=false, backup_existing=true, safety_checks=true
```

## Integration Examples

### With setup_all.py
```python
from ai_sdlc_config import ConfigManager

# Load configuration
config = ConfigManager()
config.load_hierarchy("configs/base.yml")
config.load_hierarchy(f"configs/{env}.yml")
config.merge()

# Use in installer
force = config.get_value("setup.force_overwrite")
target = config.get_value("setup.default_target")

# Run installers
if config.get_value("installation.components.claude_tasks.enabled"):
    run_claude_installer(force, target)
```

## Benefits of AI_SDLC_config

1. **Externalized Documentation**
   - Process docs live in separate markdown files
   - Easy to update without changing code
   - Can reference from multiple configs

2. **Environment Flexibility**
   - Dev vs Prod configurations
   - Runtime overrides
   - Clear merge precedence

3. **URI-Based Content**
   - Docs can be web-hosted
   - Version separately from code
   - Share across projects

4. **Dot Hierarchy**
   - Clean access: `manager.get_value("principles.test_driven.name")`
   - Wildcard searches: `manager.find_all("principles.*")`
   - Intuitive structure

---

*AI Init + AI_SDLC_config = Flexible, externalized project configuration*
