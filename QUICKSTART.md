# AI_SDLC_config Quick Start Guide

## What is AI_SDLC_config?

A library that lets you:
1. **Store configuration structure** in YAML files
2. **Store content** at any URI (files, web, S3, etc.)
3. **Merge multiple configs** with clear priority rules
4. **Access values** using simple dot notation

Think of it like C4H's config system, but **content lives at URIs** instead of being embedded.

## Installation

```bash
cd AI_SDLC_config
pip install -e .
```

## 5-Minute Tutorial

### Step 1: Create a base config

`configs/base.yml`:
```yaml
system:
  name: "My App"

agents:
  discovery:
    model: "claude-3-opus"
    prompt: "file://prompts/discovery.md"  # 👈 URI reference
```

### Step 2: Create the content file

`prompts/discovery.md`:
```markdown
# Discovery Agent

You are a discovery agent that analyzes code...
```

### Step 3: Use it in Python

```python
from ai_sdlc_config import ConfigManager

# Create manager
manager = ConfigManager()

# Load config
manager.load_hierarchy("configs/base.yml")
manager.merge()

# Get values
name = manager.get_value("system.name")
# Returns: "My App"

model = manager.get_value("agents.discovery.model")
# Returns: "claude-3-opus"

# Get URI reference
uri = manager.get_uri("agents.discovery.prompt")
# Returns: "file://prompts/discovery.md"

# Get resolved content
content = manager.get_content("agents.discovery.prompt")
# Returns: "# Discovery Agent\n\nYou are..."
```

## Priority Merging

Create environment-specific overrides:

`configs/production.yml`:
```yaml
agents:
  discovery:
    model: "claude-3-7-sonnet"  # Override base
```

```python
# Load both configs (priority: base < production)
manager.load_hierarchy("configs/base.yml")
manager.load_hierarchy("configs/production.yml")
manager.merge()

model = manager.get_value("agents.discovery.model")
# Returns: "claude-3-7-sonnet" (production wins)
```

## Runtime Overrides

Add highest-priority overrides at runtime:

```python
manager.load_hierarchy("configs/base.yml")
manager.load_hierarchy("configs/production.yml")

# Add runtime overrides (highest priority)
manager.add_runtime_overrides({
    "agents.discovery.temperature": 0.5,
    "system.debug": True
})

manager.merge()

temp = manager.get_value("agents.discovery.temperature")
# Returns: 0.5 (runtime override wins)
```

## Wildcard Searches

Find all matching paths:

```python
# Find all agents
agents = manager.find_all("agents.*")

for path, node in agents:
    print(f"{path}: {node.get_value_by_path('model')}")

# Output:
# agents.discovery: claude-3-7-sonnet
# agents.coder: claude-3-opus
# agents.solution_designer: claude-3-7-sonnet
```

## URI Schemes

### Local Files
```yaml
prompt: "file://prompts/discovery.md"
prompt: "file:///absolute/path/to/prompt.md"
```

### Web Resources
```yaml
prompt: "https://docs.company.com/prompts/v2/discovery"
```

### Cross-References
```yaml
common:
  disclaimer: "file://legal/disclaimer.md"

pages:
  home:
    footer: "ref:common.disclaimer"  # Reuse same content
```

### Custom Schemes

Register your own resolvers:

```python
def resolve_env(uri_ref):
    var_name = uri_ref.uri.replace("env://", "")
    return os.environ.get(var_name, "")

manager.register_uri_resolver("env", resolve_env)

# Now use env:// in configs
# api_key: "env://ANTHROPIC_API_KEY"
```

## Running Examples

```bash
cd examples

# Basic usage
python basic_usage.py

# Advanced features
python advanced_usage.py
```

## Key Advantages

### vs. Embedded Config (like C4H)

**Traditional (C4H)**:
```yaml
agents:
  discovery:
    prompt: |
      You are a discovery agent...
      [100 lines of embedded text]
```

**AI_SDLC_config**:
```yaml
agents:
  discovery:
    prompt: "file://prompts/discovery.md"
```

**Benefits**:
- ✅ Config file stays small
- ✅ Content can be edited separately
- ✅ Content can live on web (easy updates)
- ✅ Same content can be referenced multiple times
- ✅ Version control is cleaner

### Priority Merging

Like C4H's `deep_merge()`, but with URI preservation:

```
Layer 1: base.yml          (defaults)
Layer 2: production.yml    (environment overrides)
Layer 3: runtime overrides (highest priority)
         ↓
      Merged config
```

Later layers override earlier ones.

## Common Patterns

### Multi-Environment Setup

```
configs/
  base.yml          # Common defaults
  development.yml   # Dev overrides
  staging.yml       # Staging overrides
  production.yml    # Production overrides
```

```python
env = os.environ.get("ENV", "development")

manager.load_hierarchy("configs/base.yml")
manager.load_hierarchy(f"configs/{env}.yml")
manager.merge()
```

### Shared Content

```yaml
# base.yml
templates:
  header: "file://templates/header.html"
  footer: "file://templates/footer.html"

pages:
  home:
    header: "ref:templates.header"  # Reuse
    footer: "ref:templates.footer"  # Reuse
  about:
    header: "ref:templates.header"  # Same header
    footer: "ref:templates.footer"  # Same footer
```

### Web-Hosted Content

```yaml
prompts:
  discovery: "https://prompts.company.com/discovery/latest"
  coder: "https://prompts.company.com/coder/v2"
```

Update prompts on server without redeploying code!

## Next Steps

- **README.md** - Project overview
- **ARCHITECTURE.md** - Detailed design
- **examples/** - More usage patterns
- **CLAUDE.md** - Development guide

## Quick Reference

```python
# Create manager
manager = ConfigManager(base_path=Path("configs"))

# Load configs
manager.load_hierarchy("base.yml")
manager.load_hierarchy("production.yml")
manager.add_runtime_overrides({"key": "value"})

# Merge
manager.merge()

# Access
value = manager.get_value("path.to.key")        # Get value
uri = manager.get_uri("path.to.uri.ref")        # Get URI string
content = manager.get_content("path.to.any")    # Get resolved content
node = manager.get_node("path.to.section")      # Get sub-tree

# Search
matches = manager.find_all("path.*.pattern")    # Wildcard search

# Custom resolvers
manager.register_uri_resolver("scheme", func)   # Add custom scheme
```

Happy configuring! 🚀
