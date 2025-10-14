# AI_SDLC_config

A generic URI-based dot hierarchy configuration merging system.

## Overview

AI_SDLC_config is a standalone library that enables:
1. **URI-based content references** - Configuration nodes can reference content at any URI (file paths, URLs, etc.)
2. **Dot hierarchy navigation** - Access nested configuration using paths like `"system.agents.discovery"`
3. **Priority-based merging** - Merge multiple configuration hierarchies with override precedence
4. **Content-agnostic** - Works with any content type (YAML, Markdown, JSON, web pages, etc.)

## Core Concepts

### 1. URI References
Instead of embedding content directly in configuration files, reference URIs:

```yaml
# Traditional embedded approach (c4h)
system:
  prompts:
    discovery: |
      You are a discovery agent...
      [100 lines of text]

# New URI reference approach
system:
  prompts:
    discovery:
      uri: "file:///prompts/discovery.md"
      # or: "https://docs.example.com/prompts/discovery"
```

### 2. Dot Hierarchy
Navigate configuration using dot-delimited paths:
- `"system.prompts.discovery"` → Access discovery prompt
- `"system.agents.*"` → Wildcard match all agents
- `"*.providers.anthropic"` → Find anthropic provider in any context

### 3. Priority Merging
Merge multiple configuration sources with clear precedence:

```python
# Lower priority to higher priority
configs = [
    base_config,      # Layer 1: Defaults
    env_config,       # Layer 2: Environment-specific
    user_config,      # Layer 3: User overrides
    runtime_config    # Layer 4: Runtime overrides (highest)
]

merged = merge_hierarchies(configs)
# Result: Later configs override earlier ones
```

### 4. Lazy Content Loading
Content at URIs is loaded only when accessed, not during configuration merge.

## Inspiration

This design is inspired by the C4H configuration system (`c4h_services/src/api/service.py`) which merges YAML configurations with priority layers. AI_SDLC_config extends this concept to:
- Work with URIs instead of embedded text
- Be completely generic (no C4H dependencies)
- Support any content type (not just YAML)
- Enable distributed configuration (fetch from multiple sources)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ HierarchyNode                                       │
│ - Represents a node in dot hierarchy                │
│ - Can contain value OR uri reference                │
├─────────────────────────────────────────────────────┤
│ URIResolver                                         │
│ - Resolves URIs to content                          │
│ - Supports: file://, https://, custom schemes       │
├─────────────────────────────────────────────────────┤
│ HierarchyMerger                                     │
│ - Merges multiple hierarchies                       │
│ - Applies priority rules                            │
│ - Preserves URI references                          │
├─────────────────────────────────────────────────────┤
│ ConfigLoader                                        │
│ - Loads configuration from YAML/JSON               │
│ - Builds HierarchyNode structure                    │
└─────────────────────────────────────────────────────┘
```

## Quick Start

```python
from ai_sdlc_config import load_hierarchy, merge_hierarchies

# Load base configuration
base = load_hierarchy("config/base.yml")

# Load environment-specific overrides
prod = load_hierarchy("config/production.yml")

# Merge with priority (prod overrides base)
config = merge_hierarchies([base, prod])

# Access using dot notation
model = config.get_value("llm.agents.discovery.model")

# Get URI reference
prompt_uri = config.get_uri("llm.agents.discovery.prompt")

# Resolve and get content
prompt_content = config.get_content("llm.agents.discovery.prompt")
```

## Use Cases

1. **Multi-environment configuration** - Merge dev/staging/prod configs
2. **Distributed documentation** - Reference docs from multiple sources
3. **Content management** - Separate structure from content
4. **Version control** - Track config structure separately from content
5. **Dynamic loading** - Fetch latest content without redeploying

## Examples

### Basic Usage
See `examples/basic_usage.py` for a simple introduction.

### Advanced Features
See `examples/advanced_usage.py` for custom resolvers and merge strategies.

### Real-World Example: AI Init Integration
See `examples/ai_init_example/` for a complete example showing how to use AI_SDLC_config with the ai_init project structure:
- Multi-layer configuration (base, dev, prod)
- URI-referenced documentation
- BDD/TDD methodology configuration
- Environment-specific behavior

```bash
cd examples/ai_init_example
python ai_init_usage.py
```

## Installation

```bash
cd AI_SDLC_config
pip install -e .
```

## Project Status

✅ **Core Library Complete** - Ready for use
- HierarchyNode with dot notation
- Priority-based merging
- URI resolution (file://, http://, https://)
- YAML loader
- ConfigManager API
- Comprehensive examples

## License

TBD
