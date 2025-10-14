# AI Init + AI_SDLC_config Integration Example

This example demonstrates how the **ai_init** project structure can leverage **AI_SDLC_config** for flexible, URI-based configuration management.

## What This Demonstrates

### 1. Externalized Documentation
Instead of embedding long documents in YAML:
```yaml
# Traditional approach
methodology:
  bdd_process: |
    [300 lines of embedded text]

# AI_SDLC_config approach
methodology:
  bdd_process: "file://docs/BDD_PROCESS.md"
```

### 2. Multi-Layer Configuration
```
base.yml          → Common defaults for all environments
development.yml   → Development-specific overrides
production.yml    → Production-specific overrides
runtime           → Highest priority runtime values
```

### 3. Dot Hierarchy Access
```python
# Clean, intuitive access
name = config.get_value("principles.test_driven.name")
all_principles = config.find_all("principles.*")
```

### 4. URI Resolution
Documents can live anywhere:
- `file://` - Local filesystem
- `https://` - Web-hosted (easy updates!)
- `ref:` - Reference other config nodes

## Project Structure

```
ai_init_example/
├── configs/
│   ├── base.yml              # Base configuration
│   ├── development.yml       # Dev overrides
│   └── production.yml        # Prod overrides
├── docs/
│   ├── BDD_PROCESS.md        # Referenced by config
│   ├── QUICK_REFERENCE.md    # Referenced by config
│   └── PRINCIPLES_QUICK_CARD.md  # Referenced by config
├── ai_init_usage.py          # Demo script
└── README.md                 # This file
```

## Running the Example

```bash
# From AI_SDLC_config root
cd examples/ai_init_example
python ai_init_usage.py
```

## What You'll See

The demo shows:
1. **Configuration Loading** - Base + Dev + Runtime layers
2. **Project Information** - Name, version, environment
3. **7 Core Principles** - From dot hierarchy
4. **BDD Principles** - Behavior-first development
5. **Methodology Docs** - URI references resolved
6. **Installation Components** - Claude tasks, test dashboard
7. **Setup Config** - With runtime overrides
8. **Workflow Settings** - Auto-test, coverage requirements
9. **External URLs** - GitHub, installer links
10. **Resolved Content** - Actual doc content from URIs

## Key Concepts Demonstrated

### Configuration Layers
```python
manager.load_hierarchy("configs/base.yml")        # Layer 1
manager.load_hierarchy("configs/development.yml") # Layer 2
manager.add_runtime_overrides({...})              # Layer 3
manager.merge()  # development > base, runtime > all
```

### URI References
```yaml
# In base.yml
methodology:
  bdd_process: "file://docs/BDD_PROCESS.md"

# In code
content = manager.get_content("methodology.bdd_process")
# Automatically resolves file:// URI and returns content
```

### Dot Hierarchy
```yaml
# Nested structure
principles:
  test_driven:
    name: "Test Driven Development"
    description: "Behaviors before tests before code"
    priority: 1

# Access in code
name = manager.get_value("principles.test_driven.name")
# Returns: "Test Driven Development"
```

### Wildcard Searches
```python
# Find all principles
all_principles = manager.find_all("principles.*")

# Returns list of (path, node) tuples:
# [("principles.test_driven", node1),
#  ("principles.fail_fast", node2), ...]
```

## Real-World Use Case

### Problem: ai_init has lots of embedded documentation
```yaml
# Current ai_init approach (hypothetical)
documentation:
  bdd_process: |
    # BDD Process
    [300 lines]

  quick_reference: |
    # Quick Reference
    [200 lines]

  principles: |
    # Principles
    [150 lines]
```

### Solution: URI-based references
```yaml
# With AI_SDLC_config
documentation:
  bdd_process: "file://claude_init/claude_tasks/BDD_PROCESS.md"
  quick_reference: "file://claude_init/claude_tasks/QUICK_REFERENCE.md"
  principles: "file://claude_init/claude_tasks/PRINCIPLES_QUICK_CARD.md"
```

### Benefits
- ✅ Config file stays small and readable
- ✅ Docs can be edited independently
- ✅ Docs can be web-hosted (e.g., GitHub Pages)
- ✅ Same doc can be referenced from multiple configs
- ✅ Versioning is cleaner (config separate from content)

## Environment-Specific Behavior

### Development Environment
```yaml
# development.yml
project:
  debug_mode: true
setup:
  force_overwrite: true  # Safe to overwrite in dev
  verbose: true
installation:
  components:
    test_dashboard:
      auto_start: true     # Convenient for dev
```

### Production Environment
```yaml
# production.yml
project:
  debug_mode: false
setup:
  force_overwrite: false  # Protect files in prod
  backup_existing: true
installation:
  components:
    test_dashboard:
      auto_start: false    # Manual control in prod
```

## Integration with ai_init

This example shows how ai_init's `setup_all.py` could be enhanced:

```python
from ai_sdlc_config import ConfigManager

# Load configuration
config = ConfigManager()
config.load_hierarchy("configs/base.yml")
config.load_hierarchy(f"configs/{environment}.yml")
config.merge()

# Get installation settings
force = config.get_value("setup.force_overwrite")
target = config.get_value("setup.default_target")

# Get component settings
claude_enabled = config.get_value("installation.components.claude_tasks.enabled")
dashboard_enabled = config.get_value("installation.components.test_dashboard.enabled")

# Get methodology docs for validation
principles = config.get_content("methodology.principles")

# Run installers with config
if claude_enabled:
    run_claude_installer(force=force, target=target)
if dashboard_enabled:
    run_dashboard_installer(force=force, target=target)
```

## Comparison with Current ai_init

| Aspect | Current ai_init | With AI_SDLC_config |
|--------|----------------|---------------------|
| Config format | Python scripts | YAML with URI refs |
| Documentation | Embedded or separate | URI-referenced |
| Environment handling | Command-line flags | Config layers |
| Flexibility | Code changes needed | Config changes only |
| Version control | Mixed code+content | Separate concerns |

## Next Steps

To integrate AI_SDLC_config into ai_init:

1. **Create base configuration** - Define defaults in YAML
2. **Add environment configs** - Dev, staging, prod
3. **Reference existing docs** - Point to markdown files
4. **Update setup scripts** - Use ConfigManager
5. **Add runtime overrides** - Command-line to config

## Benefits Summary

✅ **Cleaner configs** - No embedded 300-line documents
✅ **Flexible deployment** - Docs can be web-hosted
✅ **Environment-specific** - Dev vs Prod behavior
✅ **Runtime overrides** - Command-line integration
✅ **Intuitive access** - Dot notation and wildcards
✅ **Lazy loading** - Only fetch what you need
✅ **Caching** - Efficient repeated access
✅ **Version control** - Structure separate from content

---

*This example shows AI_SDLC_config applied to the ai_init project structure*
