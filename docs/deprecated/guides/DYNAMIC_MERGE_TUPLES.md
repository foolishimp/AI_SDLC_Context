# Dynamic Merge Tuples via MCP Service

## Your Question

> "What if the experience is I want to dynamically define the tuple using the MCP service?"

**Answer**: You have TWO approaches for dynamic runtime composition.

---

## Approach 1: Runtime Overrides (Current - Recommended)

Use the `merge_projects` MCP tool to **dynamically compose** a configuration at runtime.

### Via MCP Tool

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
      "environment": "staging",
      "methodology.testing.min_coverage": 98,
      "security.vulnerability_management.scan_frequency": "hourly"
    },
    "description": "Custom runtime configuration for staging"
  }
}
```

**What this does**:
1. Merges the three projects in order (left → right priority)
2. Applies your runtime overrides (highest priority)
3. Creates a snapshot called "my_runtime_config"
4. Returns the fully merged configuration

### Via Python (ProjectRepository)

```python
from mcp_service.storage.project_repository import ProjectRepository
from pathlib import Path

repo = ProjectRepository(root_path=Path("example_projects_repo"))

# Dynamically compose a configuration
merged = repo.merge_projects(
    source_projects=[
        "ai_init_methodology",    # Priority 0
        "python_standards",        # Priority 1
        "payment_gateway"          # Priority 2
    ],
    target_name="staging_config_2025_10_16",
    runtime_overrides={
        "environment": "staging",
        "methodology.testing.min_coverage": 98,
        "security.scan_frequency": "hourly",
        "deployment.auto_deploy": False
    },
    description="Staging configuration with custom overrides"
)

print(f"Created: {merged.name}")
print(f"Merged from: {merged.merged_from}")
print(f"Runtime overrides: {merged.runtime_overrides}")
```

**Merge Order**:
```
Priority 0: ai_init_methodology
Priority 1: python_standards
Priority 2: payment_gateway
Priority 3: runtime_overrides        ← Highest priority!
```

---

## Approach 2: Pure Runtime Loading (To Be Added)

For **truly ephemeral** composition without creating a persisted snapshot, we need to add a new feature.

### Proposed: load_context_with_layers

```python
# Via ContextManager (new method to add)
context = context_manager.load_context_runtime(
    layers=[
        "ai_init_methodology",
        "python_standards",
        "payment_gateway"
    ],
    runtime_overrides={
        "environment": "production",
        "testing.min_coverage": 99
    }
)

# Returns merged context WITHOUT creating a persistent project
```

### Proposed MCP Tool: load_context_dynamic

```json
{
  "tool": "load_context_dynamic",
  "arguments": {
    "layers": [
      "ai_init_methodology",
      "python_standards",
      "payment_gateway"
    ],
    "runtime_overrides": {
      "environment": "production"
    }
  }
}
```

**Difference from Approach 1**:
- **No persistence**: Doesn't create a merged project
- **Ephemeral**: Configuration exists only in memory
- **Fast**: No git commit overhead
- **Use case**: Interactive exploration, CI/CD, testing

---

## Current Capabilities (What Exists Now)

### 1. Dynamic Tuple Composition ✅

```python
# You can dynamically specify ANY tuple
repo.merge_projects(
    source_projects=[
        "corporate_base",
        "security_baseline",
        "python_standards",
        "data_privacy_standards",
        "payment_gateway"
    ],
    target_name="ultra_secure_payment",
    runtime_overrides={
        "security.level": "maximum"
    }
)
```

**Flexible**:
- Any number of projects
- Any order
- Any runtime overrides

### 2. Runtime Overrides ✅

```python
runtime_overrides={
    # Flat keys
    "environment": "production",
    "debug": False,

    # Dot-notation keys (applied to deep paths)
    "methodology.testing.min_coverage": 99,
    "security.vulnerability_management.critical_fix_sla_hours": 2,
    "deployment.approval_chain": ["tech_lead", "cto", "ciso"],

    # Complex nested structures
    "build": {
        "version": "2.1.5",
        "timestamp": "2025-10-16T12:00:00Z",
        "commit_hash": "abc123"
    }
}
```

**Priority**: Runtime overrides are the HIGHEST priority (override everything).

### 3. Merge Provenance ✅

Every merged project stores:
- `merged_from`: Which projects were merged
- `merge_date`: When the merge happened
- `runtime_overrides`: What overrides were applied

```json
{
  "name": "staging_config",
  "project_type": "merged",
  "merged_from": [
    "ai_init_methodology",
    "python_standards",
    "payment_gateway"
  ],
  "merge_date": "2025-10-16T03:30:00Z",
  "runtime_overrides": {
    "environment": "staging",
    "testing.min_coverage": 98
  }
}
```

---

## Complete Example: Dynamic Composition

### Scenario

You want to create a **staging configuration** dynamically:
- Start with Sacred Seven methodology
- Add Python standards
- Add payment gateway requirements
- Override for staging environment

### Code

```python
from mcp_service.storage.project_repository import ProjectRepository
from pathlib import Path

repo = ProjectRepository(root_path=Path("example_projects_repo"))

# Dynamic composition
staging_config = repo.merge_projects(
    source_projects=[
        "ai_init_methodology",      # Baseline: Sacred Seven + TDD
        "python_standards",          # Python-specific standards
        "payment_gateway"            # Payment requirements
    ],
    target_name=f"payment_gateway_staging_{datetime.now().strftime('%Y%m%d_%H%M')}",
    runtime_overrides={
        # Environment
        "environment": "staging",

        # Relaxed for staging (vs production)
        "methodology.testing.min_coverage": 90,     # vs 95 for prod
        "security.vulnerability_management.critical_fix_sla_hours": 8,  # vs 4 for prod

        # Staging-specific
        "deployment.auto_deploy": True,
        "monitoring.verbose_logging": True,
        "build": {
            "environment": "staging",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    },
    description="Staging configuration with relaxed requirements"
)

print(f"✓ Created: {staging_config.name}")
print(f"  Type: {staging_config.project_type}")
print(f"  Merged from: {', '.join(staging_config.merged_from)}")
print(f"  Runtime overrides applied: {len(staging_config.runtime_overrides)} keys")
```

### Result

```
✓ Created: payment_gateway_staging_20251016_0330
  Type: merged
  Merged from: ai_init_methodology, python_standards, payment_gateway
  Runtime overrides applied: 6 keys

Stored at:
  example_projects_repo/merged_projects/payment_gateway_staging_20251016_0330/
    ├── project.json              (metadata with provenance)
    ├── config/merged.yml         (fully merged configuration)
    └── .merge_info.json          (detailed merge information)
```

---

## Use Cases

### Use Case 1: Environment-Specific Configs

```python
# Development
dev_config = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_dev",
    runtime_overrides={
        "environment": "development",
        "debug": True,
        "testing.min_coverage": 80,
        "security.level": "standard"
    }
)

# Staging
staging_config = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_staging",
    runtime_overrides={
        "environment": "staging",
        "testing.min_coverage": 90,
        "security.level": "high"
    }
)

# Production
prod_config = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_production",
    runtime_overrides={
        "environment": "production",
        "testing.min_coverage": 95,
        "security.level": "maximum",
        "deployment.approval_chain": ["tech_lead", "security_lead", "cto"]
    }
)
```

### Use Case 2: Feature Flags

```python
# Enable experimental features
experimental = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "payment_gateway"],
    target_name="payment_experimental",
    runtime_overrides={
        "features.new_fraud_detection": True,
        "features.ml_risk_scoring": True,
        "monitoring.detailed_metrics": True
    }
)
```

### Use Case 3: Team-Specific Overrides

```python
# Team A: Frontend team
frontend_config = repo.merge_projects(
    source_projects=["ai_init_methodology", "javascript_standards", "frontend_app"],
    target_name="frontend_team_a",
    runtime_overrides={
        "team": "frontend_a",
        "testing.e2e_browser": "chrome",
        "deployment.region": "us-east-1"
    }
)

# Team B: Backend team
backend_config = repo.merge_projects(
    source_projects=["ai_init_methodology", "python_standards", "api_service"],
    target_name="backend_team_b",
    runtime_overrides={
        "team": "backend_b",
        "testing.load_test_duration": 3600,
        "deployment.region": "us-west-2"
    }
)
```

### Use Case 4: CI/CD Pipeline

```python
# In your CI/CD pipeline
def build_config_for_branch(branch_name: str):
    """Dynamically create config based on git branch."""

    if branch_name == "main":
        env = "production"
        coverage = 95
    elif branch_name == "staging":
        env = "staging"
        coverage = 90
    else:
        env = "development"
        coverage = 80

    return repo.merge_projects(
        source_projects=[
            "ai_init_methodology",
            "python_standards",
            "payment_gateway"
        ],
        target_name=f"payment_{branch_name}_{build_id}",
        runtime_overrides={
            "environment": env,
            "testing.min_coverage": coverage,
            "build.branch": branch_name,
            "build.commit": git_commit_hash,
            "build.timestamp": datetime.utcnow().isoformat()
        }
    )

# Usage in CI
config = build_config_for_branch(os.environ["GIT_BRANCH"])
```

---

## Runtime Override Keys

### Flat Keys
```python
runtime_overrides={
    "environment": "production",
    "debug": False,
    "version": "2.1.0"
}
```

### Dot-Notation (Deep Path)
```python
runtime_overrides={
    "methodology.testing.min_coverage": 98,
    "security.vulnerability_management.scan_frequency": "continuous",
    "deployment.approval_chain": ["lead", "manager"]
}
```

### Nested Structures
```python
runtime_overrides={
    "build": {
        "version": "2.1.0",
        "timestamp": "2025-10-16T12:00:00Z",
        "environment": "production"
    },
    "deployment": {
        "strategy": "blue-green",
        "rollback_enabled": True
    }
}
```

---

## Merge Priority with Runtime Overrides

```
Priority 0: ai_init_methodology        (lowest)
    ↓
Priority 1: python_standards
    ↓
Priority 2: payment_gateway
    ↓
Priority 3: runtime_overrides          (highest - wins all conflicts!)
```

**Example**:
```python
# ai_init_methodology: min_coverage = 80
# python_standards:    min_coverage = 85
# payment_gateway:     min_coverage = 95
# runtime_overrides:   min_coverage = 98

# Final result: 98 (runtime wins!)
```

---

## Accessing Dynamic Configurations

### Load the Merged Project

```python
# After creating with merge_projects
merged_config = repo.get_project_config("payment_gateway_staging_20251016_0330")

# Access values
coverage = merged_config.get_value("methodology.testing.min_coverage")
# Returns: 98 (from runtime_overrides)

env = merged_config.get_value("environment")
# Returns: "staging" (from runtime_overrides)
```

### Via Context Manager

```python
from mcp_service.server.context_tools import ContextManager

context_mgr = ContextManager(repository=repo)

# Load the merged project
context = context_mgr.load_context("payment_gateway_staging_20251016_0330")

# Access merged values
print(context["requirements"]["testing"]["min_coverage"])
# Output: 98

print(context["environment"])
# Output: staging
```

---

## Implementing Pure Runtime Loading (Optional Enhancement)

If you want **truly ephemeral** loading without persisting merged projects:

### Add to ContextManager

```python
# In context_tools.py
def load_context_runtime(
    self,
    layers: List[str],
    runtime_overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Load context dynamically from layers without persisting.

    Args:
        layers: List of project names to merge (priority order)
        runtime_overrides: Additional runtime overrides

    Returns:
        Merged context dictionary
    """
    # Create temporary ConfigManager
    from ai_sdlc_config import ConfigManager

    manager = ConfigManager(base_path=self.repo.root_path)

    # Load each layer
    for layer_name in layers:
        project_path = self.repo.root_path / layer_name
        config_file = project_path / "config" / "config.yml"
        if config_file.exists():
            rel_path = config_file.relative_to(self.repo.root_path)
            manager.load_hierarchy(str(rel_path))

    # Apply runtime overrides
    if runtime_overrides:
        manager.add_runtime_overrides(runtime_overrides)

    # Merge
    manager.merge()

    # Build context dictionary (same as load_context)
    context = self._build_context_dict(manager)
    context["_runtime_layers"] = layers
    context["_runtime_overrides"] = runtime_overrides

    self.current_context = context
    return context
```

### Add MCP Tool

```python
# In main.py
Tool(
    name="load_context_runtime",
    description="Load context dynamically from layers without persisting",
    inputSchema={
        "type": "object",
        "properties": {
            "layers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Project names to merge (priority order)"
            },
            "runtime_overrides": {
                "type": "object",
                "description": "Runtime overrides (highest priority)"
            }
        },
        "required": ["layers"]
    }
)
```

### Usage

```python
# Ephemeral loading - no persistence
context = context_manager.load_context_runtime(
    layers=[
        "ai_init_methodology",
        "python_standards",
        "payment_gateway"
    ],
    runtime_overrides={
        "environment": "production",
        "testing.min_coverage": 99
    }
)

# Context exists in memory only, not saved to disk
```

---

## Summary

### What You Can Do NOW ✅

**Dynamic tuple composition with `merge_projects`**:
```python
repo.merge_projects(
    source_projects=["a", "b", "c"],     # Your tuple
    target_name="my_config",
    runtime_overrides={...}               # Your overrides
)
```

**Benefits**:
- ✅ Fully dynamic - specify tuple at runtime
- ✅ Runtime overrides (highest priority)
- ✅ Merge provenance tracked
- ✅ Reproducible (saved snapshot)
- ✅ Available via MCP tool

**Limitation**:
- Creates a persistent merged project (git commit)

### What to ADD (Optional) 🔄

**Ephemeral runtime loading**:
```python
context_manager.load_context_runtime(
    layers=["a", "b", "c"],
    runtime_overrides={...}
)
```

**Benefits**:
- ✅ No persistence
- ✅ Fast (no git overhead)
- ✅ Perfect for exploration

**Trade-off**:
- ❌ Not saved (must recreate)
- ❌ No provenance tracking

---

## Recommendation

**For most use cases**: Use `merge_projects` (Approach 1)
- Dynamic composition ✅
- Runtime overrides ✅
- Persistence & provenance ✅
- Already implemented ✅

**For ephemeral exploration**: Add `load_context_runtime` (Approach 2)
- Quick, no-commit option
- Good for testing/CI/CD
- Requires implementation

---

*Your system already supports dynamic tuple definition! 🎯*
