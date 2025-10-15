# Dynamic Tuples - Quick Reference

## Question: How do I dynamically define the merge tuple using MCP?

**Answer**: Use the `merge_projects` tool with `runtime_overrides`.

---

## Quick Example

```python
from mcp_service.storage.project_repository import ProjectRepository

repo = ProjectRepository(root_path=Path("example_projects_repo"))

# Dynamically define your tuple
config = repo.merge_projects(
    source_projects=[
        "ai_init_methodology",    # Your baseline
        "python_standards",        # Your standards
        "payment_gateway"          # Your project
    ],
    target_name="my_config",
    runtime_overrides={
        "environment": "staging",
        "testing.min_coverage": 98
    }
)
```

**Merge order**: Left to right + runtime overrides (highest priority)

---

## Via MCP Tool

```json
{
  "tool": "merge_projects",
  "arguments": {
    "source_projects": [
      "ai_init_methodology",
      "python_standards",
      "payment_gateway"
    ],
    "target_project": "my_runtime_config",
    "runtime_overrides": {
      "environment": "production",
      "methodology.testing.min_coverage": 99
    }
  }
}
```

---

## Use Cases

### 1. Environment-Specific Configs

```python
# Development
dev = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_dev",
    runtime_overrides={
        "environment": "development",
        "testing.min_coverage": 80,   # Relaxed
        "debug": True
    }
)

# Production
prod = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_prod",
    runtime_overrides={
        "environment": "production",
        "testing.min_coverage": 99,   # Strict
        "security.level": "maximum"
    }
)
```

**Same tuple, different overrides!**

### 2. CI/CD Pipeline

```python
def create_config_for_branch(branch: str, build_id: str):
    """Dynamically create config based on git branch."""

    if branch == "main":
        env, coverage = "production", 99
    elif branch == "staging":
        env, coverage = "staging", 90
    else:
        env, coverage = "development", 80

    return repo.merge_projects(
        source_projects=[
            "ai_init_methodology",
            "python_standards",
            "payment_gateway"
        ],
        target_name=f"payment_{branch}_{build_id}",
        runtime_overrides={
            "environment": env,
            "testing.min_coverage": coverage,
            "build.branch": branch,
            "build.id": build_id
        }
    )
```

### 3. Feature Flags

```python
# Enable experimental features
experimental = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_experimental",
    runtime_overrides={
        "features.new_fraud_detection": True,
        "features.ml_risk_scoring": True
    }
)
```

---

## Runtime Override Priority

```
Priority 0: ai_init_methodology    (lowest)
    ↓
Priority 1: python_standards
    ↓
Priority 2: payment_gateway
    ↓
Priority 3: runtime_overrides      (HIGHEST - wins everything!)
```

**Example**:
```python
# payment_gateway: min_coverage = 95
# runtime_overrides: min_coverage = 99

# Result: 99 (runtime wins!)
```

---

## Runtime Override Formats

### Flat Keys
```python
runtime_overrides={
    "environment": "production",
    "debug": False
}
```

### Dot-Notation (Deep Paths)
```python
runtime_overrides={
    "methodology.testing.min_coverage": 99,
    "security.vulnerability_management.scan_frequency": "continuous"
}
```

### Nested Structures
```python
runtime_overrides={
    "build": {
        "version": "2.1.0",
        "timestamp": "2025-10-16T12:00:00Z",
        "environment": "production"
    }
}
```

---

## What Gets Created

```
example_projects_repo/
└── merged_projects/
    └── my_config/
        ├── project.json          # Metadata with provenance
        ├── config/
        │   └── merged.yml       # Fully merged configuration
        └── .merge_info.json     # Merge details
```

**Provenance tracked**:
- Which projects were merged
- When the merge happened
- What runtime overrides were applied

---

## Accessing the Config

### Load It

```python
# Get the merged configuration
config_manager = repo.get_project_config("my_config")

# Access values
coverage = config_manager.get_value("methodology.testing.min_coverage")
env = config_manager.get_value("environment")
```

### Via Context Manager

```python
from mcp_service.server.context_tools import ContextManager

context_mgr = ContextManager(repository=repo)
context = context_mgr.load_context("my_config")

# Access merged values
print(context["requirements"]["testing"]["min_coverage"])
```

---

## Benefits

✅ **Fully Dynamic**: Specify tuple at runtime (not in project.json)
✅ **Flexible**: Any combination, any order
✅ **Runtime Overrides**: Highest priority (override everything)
✅ **Provenance**: Track what was merged and when
✅ **Reproducible**: Saved snapshot for deployments
✅ **Available via MCP**: Use from Claude or any MCP client

---

## Key Difference: Static vs Dynamic

### Static (project.json)
```json
{
  "name": "payment_gateway",
  "base_projects": [
    "ai_init_methodology",
    "python_standards"
  ]
}
```
**Fixed** at project creation time.

### Dynamic (runtime)
```python
repo.merge_projects(
    source_projects=[
        "ai_init_methodology",
        "python_standards",
        "payment_gateway"
    ],
    runtime_overrides={...}
)
```
**Flexible** - decide at runtime!

---

## When to Use

### Use Dynamic Tuples For:
- CI/CD pipelines (per branch/environment)
- Environment-specific configs
- Feature flags & A/B testing
- Build snapshots
- Team-specific configs

### Use Static base_projects For:
- Permanent project inheritance
- Core project structure
- Reusable base layers

---

## Try It

```bash
# Run the example
cd mcp_service/examples
python dynamic_tuple_example.py
```

**Output**: Creates dev, staging, and prod configs dynamically!

---

*Full guide: [DYNAMIC_MERGE_TUPLES.md](DYNAMIC_MERGE_TUPLES.md)*
