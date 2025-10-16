# AI_SDLC_Context

A generic URI-based dot hierarchy configuration merging system, built with the **Sacred Seven** methodology from [ai_init](https://github.com/foolishimp/ai_init).

**Mantra**: **"Excellence or nothing"** 🔥

## Overview

AI_SDLC_Context is a standalone library that enables:
1. **URI-based content references** - Configuration nodes can reference content at any URI (file paths, URLs, etc.)
2. **Dot hierarchy navigation** - Access nested configuration using paths like `"system.agents.discovery"`
3. **Priority-based merging** - Merge multiple configuration hierarchies with override precedence
4. **Content-agnostic** - Works with any content type (YAML, Markdown, JSON, web pages, etc.)

**Built with**: Test-Driven Development, 156 tests (100% passing), comprehensive coverage

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

This design is inspired by the C4H configuration system (`c4h_services/src/api/service.py`) which merges YAML configurations with priority layers. AI_SDLC_Context extends this concept to:
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

## Contexts and Examples

### Baseline Contexts ([contexts/](contexts/))

**Read-only reference contexts** provided by AI_SDLC_Context:
- **aisdlc_methodology/** - Sacred Seven principles and TDD workflow
- **python_standards/** - Python language standards and best practices

These contexts can be served by MCP context servers and composed via **context tuples**.

See [contexts/README.md](contexts/README.md) for details.

---

### Example Projects ([examples/](examples/))

**Example local projects** demonstrating federated context usage:
- **acme_corporate/** - Example corporate-level policies
- **payment_gateway/** - Example high-risk enterprise project
- **admin_dashboard/** - Example low-risk internal tool

**Key demonstrations**:
1. **Federated contexts** - Load from multiple MCP servers (corporate, division, local)
2. **Context tuples** - Compose layers with priority-based merging
3. **Multi-layer inheritance** - Corporate → Division → Team → Project
4. **Local customization** - Override baseline contexts for specific needs

See [examples/README.md](examples/README.md) for comprehensive federated context guide.

## MCP Service

AI_SDLC_Context includes a **Model Context Protocol (MCP) service** that provides:

1. **Project Management** - Create, read, update, delete configuration projects
2. **Content Management** - Add/remove nodes, documents
3. **Merge Operations** - Merge multiple projects to create deployment-ready configs
4. **LLM Inspection** - Query projects using natural language via LLM
5. **Git-Backed Storage** - All changes tracked in version control

### Key Concepts: Custom vs Merged Projects

**Custom Override Project** (e.g., `payment_service`):
- Manually created YAML configuration
- Contains only explicit overrides
- Inherits from base projects at runtime
- Living configuration for active development

**Merged Project** (e.g., `payment_service_production`):
- Auto-generated from merge operation
- Contains full merged configuration
- Includes merge metadata (sources, date, overrides)
- Immutable snapshot for deployment

### Running the MCP Service

```bash
# Install dependencies
cd mcp_service
pip install -r requirements.txt

# Start MCP server (stdio mode for Claude Desktop)
python -m server.main

# Or specify custom repository path
python -m server.main --repo-path /path/to/projects_repo
```

### Using with Claude Desktop

Add to Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ai-sdlc-config": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "/Users/jim/src/apps/AI_SDLC_Context/mcp_service"
    }
  }
}
```

### MCP Service Examples

```bash
# Direct usage example (without MCP protocol)
cd mcp_service/examples
python direct_usage_example.py

# MCP client example (requires MCP server running)
python mcp_client_example.py
```

See `mcp_service/README.md` for complete MCP service documentation.

## Installation

```bash
cd AI_SDLC_Context
pip install -e .
```

## Development Methodology

This project follows the **Sacred Seven** principles from [ai_init](https://github.com/foolishimp/ai_init):

1. **Test Driven Development** - "No code without tests"
2. **Fail Fast & Root Cause** - "Break loudly, fix completely"
3. **Modular & Maintainable** - "Single responsibility, loose coupling"
4. **Reuse Before Build** - "Check first, create second"
5. **Open Source First** - "Suggest alternatives, human decides"
6. **No Legacy Baggage** - "Clean slate, no debt"
7. **Perfectionist Excellence** - "Best of breed only"

👉 **Full Methodology**: [aisdlc_methodology](contexts/aisdlc_methodology/)

### TDD Workflow

**RED → GREEN → REFACTOR**

All code follows Test-Driven Development:
- 156 unit tests (100% passing)
- Comprehensive test coverage
- Tests written first, always
- Execution time: ~0.16 seconds

👉 **Test Suite**: [tests/](tests/)

## Project Status

✅ **Core Library Complete** - Production ready
- HierarchyNode with dot notation ✅
- Priority-based merging ✅
- URI resolution (file://, http://, https://) ✅
- YAML loader ✅
- ConfigManager API ✅
- Comprehensive examples ✅
- **156 passing tests** ✅
- **Sacred Seven compliant** ✅

## Related Projects

- **[ai_init](https://github.com/foolishimp/ai_init)** - Baseline methodology (origin of Sacred Seven)
- **[AI_INIT_REVIEW.md](AI_INIT_REVIEW.md)** - Detailed comparison and evolution

## License

TBD
