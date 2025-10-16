# AI SDLC Context Plugins

This directory contains **Claude Code plugins** that provide baseline development contexts and methodologies.

## Available Plugins

### aisdlc-methodology
**Core development methodology** - Sacred Seven principles and TDD workflow
- Sacred Seven development principles
- TDD workflow (RED → GREEN → REFACTOR)
- Pair programming practices
- Session management guides
- Task documentation templates

**Dependencies**: None (foundation plugin)

---

### python-standards
**Python language standards** - PEP 8, pytest, type hints, tooling
- PEP 8 style guidelines
- Python testing practices (pytest)
- Type hints and documentation standards
- Python tooling (black, mypy, pylint)

**Dependencies**: `aisdlc-methodology`

---

## Using These Plugins

### Option 1: Add This Marketplace (Recommended)

Add this repository as a Claude Code marketplace:

```bash
# In Claude Code
/plugin marketplace add foolishimp/AI_SDLC_Context
```

Or in your `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "aisdlc": {
      "source": {
        "source": "github",
        "repo": "foolishimp/AI_SDLC_Context"
      }
    }
  }
}
```

Then install plugins:

```bash
/plugin install @aisdlc/aisdlc-methodology
/plugin install @aisdlc/python-standards
```

### Option 2: Local Installation

Clone this repository and add as local marketplace:

```bash
git clone https://github.com/foolishimp/AI_SDLC_Context.git
cd your-project
/plugin marketplace add ../AI_SDLC_Context
/plugin install aisdlc-methodology
```

---

## Federated Approach

Use **multiple marketplaces** for organizational hierarchy:

### Corporate Marketplace
```json
{
  "extraKnownMarketplaces": {
    "corporate": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-contexts"
      }
    }
  },
  "plugins": [
    "@corporate/aisdlc-methodology",
    "@corporate/python-standards"
  ]
}
```

### Division Marketplace (Extends Corporate)
```json
{
  "extraKnownMarketplaces": {
    "corporate": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-contexts"
      }
    },
    "division": {
      "source": {
        "source": "git",
        "url": "https://git.company.com/eng-division/plugins.git"
      }
    }
  },
  "plugins": [
    "@corporate/aisdlc-methodology",
    "@corporate/python-standards",
    "@division/backend-standards"
  ]
}
```

### Local Project (Extends Division)
```json
{
  "extraKnownMarketplaces": {
    "corporate": {
      "source": {"source": "github", "repo": "acme-corp/claude-contexts"}
    },
    "division": {
      "source": {"source": "git", "url": "https://git.company.com/eng-division/plugins.git"}
    },
    "local": {
      "source": {"source": "local", "path": "./my-contexts"}
    }
  },
  "plugins": [
    "@corporate/aisdlc-methodology",
    "@corporate/python-standards",
    "@division/backend-standards",
    "@local/my-project-context"
  ]
}
```

**Plugin loading order** determines override priority - later plugins can override earlier ones.

---

## Creating Your Own Context Plugin

### 1. Create Plugin Structure

```bash
mkdir -p my-project-context/.claude-plugin
mkdir -p my-project-context/config
mkdir -p my-project-context/commands
```

### 2. Create plugin.json

```json
{
  "name": "my-project-context",
  "version": "1.0.0",
  "displayName": "My Project Context",
  "description": "Project-specific configuration and standards",
  "dependencies": {
    "aisdlc-methodology": "^1.0.0",
    "python-standards": "^1.0.0"
  }
}
```

### 3. Create config/context.yml

```yaml
project:
  name: "my-payment-api"
  type: "api_service"
  risk_level: "high"

# Override baseline standards
testing:
  coverage_minimum: 95  # Higher than baseline 80%

security:
  penetration_testing: required
  pci_compliance: true
```

### 4. Add to Local Marketplace

```bash
# In your project
mkdir .claude-plugins
mv my-project-context .claude-plugins/

# In .claude/settings.json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "local",
        "path": "./.claude-plugins"
      }
    }
  },
  "plugins": [
    "@aisdlc/aisdlc-methodology",
    "@aisdlc/python-standards",
    "@local/my-project-context"
  ]
}
```

---

## Plugin Structure

Each plugin follows this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── config/
│   ├── context.yml         # Context configuration (YAML)
│   └── overrides.yml       # Optional overrides
├── commands/                # Slash commands (optional)
│   └── load-context.md
├── docs/                    # Documentation
│   ├── README.md
│   ├── guides/
│   └── principles/
└── project.json            # Legacy: for MCP service compatibility
```

---

## Comparison: Old vs New Approach

### Old Approach (Complex)
- Custom MCP service with federated servers
- Context tuples: `corporate.aisdlc_methodology`
- Custom merging logic
- URI resolution system
- Complex project initialization

### New Approach (Simplified)
- Native Claude Code marketplaces
- Plugin system: `@corporate/aisdlc-methodology`
- Claude handles plugin loading/composition
- Standard plugin structure
- Simple: add marketplace, install plugins

**Result**: 90% less complexity, same functionality!

---

## For Non-Claude LLMs (Codex, Gemini, etc.)

Use the **MCP service** (fallback):

```bash
# Start MCP context service
python -m mcp_service.server --port 8000 --plugins-dir plugins/

# MCP clients (non-Claude) can connect and query contexts
# See mcp_service/docs/ for details
```

---

## Migration Guide

### From example_projects_repo/ to plugins/

Old structure:
```
example_projects_repo/aisdlc_methodology/
```

New structure:
```
plugins/aisdlc-methodology/    # Note: kebab-case
├── .claude-plugin/plugin.json
└── (rest of files same)
```

### From Context Tuples to Plugins

Old (custom):
```json
{
  "context_tuple": [
    "corporate.aisdlc_methodology",
    "local.my_project"
  ]
}
```

New (Claude Code):
```json
{
  "plugins": [
    "@corporate/aisdlc-methodology",
    "@local/my-project-context"
  ]
}
```

---

## Benefits

✅ **Simpler** - Use Claude Code's native plugin system
✅ **Standard** - Follow Claude Code conventions
✅ **Federated** - Multiple marketplaces (corporate, division, local)
✅ **Composable** - Plugin loading order = merge priority
✅ **Portable** - Export marketplace to GitHub/Git for sharing
✅ **Fallback** - MCP service still available for non-Claude LLMs

---

## See Also

- [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins)
- [Marketplace Guide](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MCP Service](../mcp_service/) - For non-Claude LLMs
- [Examples](../examples/) - Example local context plugins
