# CLAUDE.md - AI_SDLC_Context Project Guide

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**AI_SDLC_Context** is a generic URI-based dot hierarchy configuration merging system.

### Purpose

Enable flexible configuration management where:
1. Content can exist at any URI (files, web, S3, etc.)
2. Configuration structure uses dot notation (`"system.agents.discovery"`)
3. Multiple configurations can be merged with clear priority
4. Content is loaded lazily (only when accessed)

### Inspiration

Inspired by the C4H configuration system (`c4h/config/system_config.yml` and `c4h_agents/config.py`) but designed to be:
- **Generic** - No domain-specific logic
- **URI-based** - Content referenced, not embedded
- **Extensible** - Custom URI schemes supported

## Project Structure

```
AI_SDLC_Context/
├── src/ai_sdlc_config/
│   ├── models/                 # Data structures
│   │   └── hierarchy_node.py   # HierarchyNode, URIReference
│   ├── loaders/                # Loading configurations
│   │   ├── yaml_loader.py      # Parse YAML → HierarchyNode
│   │   └── uri_resolver.py     # Resolve URIs → content
│   ├── mergers/                # Merge logic
│   │   └── hierarchy_merger.py # Priority-based merging
│   └── core/                   # High-level API
│       └── config_manager.py   # ConfigManager (main interface)
├── examples/
│   ├── configs/                # Example YAML configs
│   ├── prompts/                # Example referenced content
│   ├── basic_usage.py          # Simple demo
│   └── advanced_usage.py       # Advanced features demo
├── tests/                      # Unit tests (TODO)
├── docs/                       # Documentation
├── README.md                   # Project overview
├── ARCHITECTURE.md             # Detailed design doc
└── setup.py                    # Installation
```

## Core Concepts

### 1. HierarchyNode

The fundamental data structure representing a node in the configuration tree.

```python
@dataclass
class HierarchyNode:
    path: str                           # Dot-delimited path
    value: Optional[NodeValue] = None   # Can be URIReference
    children: Dict[str, HierarchyNode]  # Nested nodes
    source: Optional[str] = None        # Origin tracking
    priority: int = 0                   # Merge priority
```

### 2. URIReference

Represents a reference to content at a URI.

```python
@dataclass
class URIReference:
    uri: str                    # e.g., "file://prompts/discovery.md"
    scheme: URIScheme          # file, http, https, data, ref
    content_type: Optional[str]
    metadata: Dict[str, Any]
```

### 3. Priority Merging

Multiple configurations are merged with clear precedence:

```python
# Lower priority → Higher priority
configs = [base, production, runtime]
merged = merger.merge(configs)
# Result: runtime > production > base
```

## Common Operations

### Running Examples

```bash
# Basic usage example
cd examples
python basic_usage.py

# Advanced features example
python advanced_usage.py
```

### Using the Library

```python
from ai_sdlc_config import ConfigManager

# Create manager
manager = ConfigManager(base_path=Path("configs"))

# Load configurations (priority order)
manager.load_hierarchy("base.yml")
manager.load_hierarchy("production.yml")
manager.add_runtime_overrides({"system.debug": True})

# Merge all layers
manager.merge()

# Access values
value = manager.get_value("system.agents.discovery.model")
uri = manager.get_uri("system.agents.discovery.prompt")
content = manager.get_content("system.agents.discovery.prompt")

# Wildcard search
agents = manager.find_all("system.agents.*")
```

### Testing

```bash
# Run tests (when implemented)
pytest tests/

# Run with coverage
pytest --cov=ai_sdlc_config tests/
```

## Key Design Principles

### 1. Separation of Structure and Content

**Structure** (in YAML):
```yaml
agents:
  discovery:
    prompt: "file://prompts/discovery.md"
```

**Content** (at URI):
```markdown
# Discovery Agent Prompt
You are a discovery agent...
```

### 2. Lazy Resolution

URIs are not resolved during merge - only when `get_content()` is called.

### 3. Priority Override

Later configurations override earlier ones:
- Base config provides defaults
- Environment config overrides for specific environments
- Runtime config has highest priority

### 4. No Domain Coupling

Unlike C4H which is specific to LLM agents, this library is generic and can be used for any configuration needs.

## Extension Points

### Custom URI Schemes

```python
def resolve_s3(uri_ref: URIReference) -> str:
    # Fetch from AWS S3
    bucket, key = parse_s3_uri(uri_ref.uri)
    return s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()

manager.register_uri_resolver("s3", resolve_s3)
```

### Custom Merge Strategies

```python
class CustomStrategy(MergeStrategy):
    CONCATENATE = "concatenate"  # Combine instead of override
```

## Comparison with C4H

| Feature | C4H | AI_SDLC_Context |
|---------|-----|----------------|
| Dot notation | ✅ | ✅ |
| Priority merging | ✅ | ✅ |
| Content storage | Embedded in YAML | Referenced by URI |
| Content types | YAML values | Any content at any URI |
| Domain | LLM agents | Generic |
| Loading | Eager | Lazy |

## Development Methodology

**IMPORTANT**: This project follows the **Sacred Seven** principles from [ai_init](https://github.com/foolishimp/ai_init).

### The Sacred Seven

1. **Test Driven Development** - "No code without tests"
2. **Fail Fast & Root Cause** - "Break loudly, fix completely"
3. **Modular & Maintainable** - "Single responsibility, loose coupling"
4. **Reuse Before Build** - "Check first, create second"
5. **Open Source First** - "Suggest alternatives, human decides"
6. **No Legacy Baggage** - "Clean slate, no debt"
7. **Perfectionist Excellence** - "Best of breed only"

**Ultimate Mantra**: **"Excellence or nothing"** 🔥

👉 **Read Full Methodology**: [methodology/](methodology/)
- [Sacred Seven Principles](methodology/principles/SACRED_SEVEN.md)
- [TDD Workflow](methodology/processes/TDD_WORKFLOW.md)

### TDD Workflow

**Always follow**: RED → GREEN → REFACTOR

1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve code quality
4. **COMMIT**: Save with clear message
5. **REPEAT**: Next test

**No code without tests. Ever.**

### Before You Code

Ask these seven questions:

1. Have I written tests first? (Principle #1)
2. Will this fail loudly if wrong? (Principle #2)
3. Is this module focused? (Principle #3)
4. Did I check if this exists? (Principle #4)
5. Have I researched alternatives? (Principle #5)
6. Am I avoiding tech debt? (Principle #6)
7. Is this excellent? (Principle #7)

**If not "yes" to all seven, don't code yet.**

## Development Guidelines

### Adding New URI Schemes

1. **RED**: Write test for new scheme → Should FAIL
2. Add scheme to `URIScheme` enum in `models/hierarchy_node.py`
3. Implement resolver method in `URIResolver` class
4. **GREEN**: Tests should PASS
5. **REFACTOR**: Clean up implementation
6. Document in README.md
7. **COMMIT**: Save with tests

### Modifying Merge Logic

1. **RED**: Write test for new behavior → Should FAIL
2. Update logic in `mergers/hierarchy_merger.py`
3. Core method: `_merge_two_nodes(base, override, priority)`
4. **GREEN**: Tests should PASS
5. **REFACTOR**: Improve implementation
6. Add edge case tests
7. **COMMIT**: Save with tests

### Code Standards

- **Tests first** (always RED → GREEN → REFACTOR)
- Use type hints
- Follow PEP 8
- Add docstrings to all public methods
- Keep functions focused and small
- No technical debt
- Excellence or nothing

## Related Projects

- **C4H** (`/Users/jim/src/apps/c4h`) - Inspiration for this project
- Similar pattern: Structure + content separation
- Similar API: Dot notation, priority merging
- Key difference: C4H embeds content, we reference it

## Future Enhancements

See ARCHITECTURE.md "Future Enhancements" section for planned features:
- Async URI resolution
- Content validation
- Cache persistence
- Hot reload
- Visual tools

## Questions?

- See `README.md` for quick start
- See `ARCHITECTURE.md` for detailed design
- See `examples/` for usage patterns
- Ask Claude Code for help!
