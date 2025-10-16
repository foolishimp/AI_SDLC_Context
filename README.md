# AI_SDLC_Context

**Claude Code Plugin Marketplace** for baseline development contexts and methodologies.

**Mantra**: **"Excellence or nothing"** 🔥

---

## What Is This?

A **Claude Code marketplace** providing baseline development contexts that you can install as plugins:

- **aisdlc-methodology** - Sacred Seven principles and TDD workflow
- **python-standards** - Python language standards (PEP 8, pytest, type hints)
- *(More language standards and contexts coming)*

These contexts can be composed in a **federated architecture**: corporate → division → team → project.

---

## Quick Start

### 1. Add This Marketplace

In Claude Code:

```bash
/plugin marketplace add foolishimp/AI_SDLC_Context
```

Or add to your `.claude/settings.json`:

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

### 2. Install Plugins

```bash
/plugin install @aisdlc/aisdlc-methodology
/plugin install @aisdlc/python-standards
```

### 3. Start Coding!

The contexts are now active. Claude will follow the Sacred Seven principles and Python standards automatically.

---

## Federated Architecture

The power of this approach is **multiple marketplaces** for organizational hierarchy:

```json
{
  "extraKnownMarketplaces": {
    "corporate": {
      "source": {"source": "github", "repo": "acme-corp/claude-contexts"}
    },
    "division": {
      "source": {"source": "git", "url": "https://git.company.com/eng/plugins.git"}
    },
    "local": {
      "source": {"source": "local", "path": "./my-contexts"}
    }
  },
  "plugins": [
    "@corporate/aisdlc-methodology",      // Corporate baseline
    "@corporate/python-standards",         // Corporate Python standards
    "@division/backend-standards",         // Division overrides
    "@local/my-team-customizations",       // Team customizations
    "@local/my-project-context"            // Project-specific
  ]
}
```

**Plugin loading order** = merge priority. Later plugins override earlier ones.

---

## Available Plugins

### aisdlc-methodology

**Core development methodology** - Foundation for all projects

**Provides**:
- **Sacred Seven Principles**
  1. Test Driven Development - "No code without tests"
  2. Fail Fast & Root Cause - "Break loudly, fix completely"
  3. Modular & Maintainable - "Single responsibility, loose coupling"
  4. Reuse Before Build - "Check first, create second"
  5. Open Source First - "Suggest alternatives, human decides"
  6. No Legacy Baggage - "Clean slate, no debt"
  7. Perfectionist Excellence - "Best of breed only"

- **TDD Workflow**: RED → GREEN → REFACTOR → COMMIT
- **Pair Programming Practices**: Human-AI collaboration guide
- **Session Management**: Session starter checklists
- **Task Documentation**: Templates for finished tasks

**Dependencies**: None (foundation)

👉 [Full Documentation](plugins/aisdlc-methodology/docs/)

---

### python-standards

**Python language standards** - PEP 8, pytest, type hints, tooling

**Provides**:
- PEP 8 style guidelines
- Python testing practices (pytest, coverage >80%)
- Type hints and docstring standards
- Tooling configuration (black, mypy, pylint, pytest)
- Python project structure best practices

**Dependencies**: `aisdlc-methodology`

👉 [Full Documentation](plugins/python-standards/)

---

## Creating Your Own Context Plugin

See [plugins/README.md](plugins/README.md) for complete guide.

### Quick Example

```bash
# Create plugin structure
mkdir -p my-project/.claude-plugin
cd my-project

# Create plugin.json
cat > .claude-plugin/plugin.json <<EOF
{
  "name": "my-project-context",
  "version": "1.0.0",
  "displayName": "My Project",
  "dependencies": {
    "aisdlc-methodology": "^1.0.0",
    "python-standards": "^1.0.0"
  }
}
EOF

# Create config
mkdir config
cat > config/context.yml <<EOF
project:
  name: "my-payment-api"
  risk_level: "high"

testing:
  coverage_minimum: 95  # Override baseline 80%

security:
  pci_compliance: required
EOF

# Add to local marketplace
/plugin marketplace add ./my-project
/plugin install my-project-context
```

---

## Use Cases

### Corporate Standard Contexts

Your company hosts a marketplace with baseline contexts:

```
corporate-marketplace/
├── aisdlc-methodology/
├── python-standards/
├── javascript-standards/
├── security-baseline/
└── compliance-requirements/
```

All developers add this marketplace and get company standards.

### Division Customizations

Engineering division extends corporate with specific practices:

```
division-marketplace/
├── backend-api-standards/      # Extends python-standards
├── frontend-standards/          # Extends javascript-standards
└── microservices-patterns/
```

### Team/Project Contexts

Individual teams create local contexts:

```
.claude-plugins/
├── team-conventions/
└── project-specific/
```

### Result: Layered Composition

```
Corporate (baseline)
  └─> Division (extensions)
      └─> Team (customizations)
          └─> Project (specifics)
```

Each layer can override the previous, creating a flexible hierarchy.

---

## For Non-Claude LLMs

This repository also includes an **MCP service** for non-Claude Code LLMs (Codex, Gemini, etc.):

```bash
python -m mcp_service.server --port 8000 --plugins-dir plugins/
```

See [mcp_service/docs/](mcp_service/docs/) for details.

**For Claude Code users**: Just use the marketplace approach (simpler!).

---

## Sacred Seven Methodology

All code in this project follows the Sacred Seven principles:

1. **Test Driven Development** - "No code without tests"
   - 156 unit tests (100% passing)
   - Comprehensive test coverage
   - Tests written first, always

2. **Fail Fast & Root Cause** - "Break loudly, fix completely"
   - No workarounds
   - Fix root causes
   - Clear error messages

3. **Modular & Maintainable** - "Single responsibility, loose coupling"
   - Small, focused modules
   - Clear separation of concerns
   - Easy to understand and extend

4. **Reuse Before Build** - "Check first, create second"
   - Leverage Claude Code's plugin system
   - Use native marketplace federation
   - Build only what's unique

5. **Open Source First** - "Suggest alternatives, human decides"
   - Transparent development
   - Community-driven
   - Open to contributions

6. **No Legacy Baggage** - "Clean slate, no debt"
   - Removed 90% of custom complexity
   - Leveraged native Claude Code features
   - Clean, simple architecture

7. **Perfectionist Excellence** - "Best of breed only"
   - High-quality code
   - Comprehensive documentation
   - Production-ready

👉 **Full Methodology**: [aisdlc-methodology plugin](plugins/aisdlc-methodology/)

---

## Project Structure

```
AI_SDLC_Context/
├── plugins/                     # Claude Code plugins
│   ├── aisdlc-methodology/     # Core methodology
│   ├── python-standards/       # Python standards
│   └── README.md               # Plugin guide
│
├── examples/                    # Example local contexts
│   ├── local_projects/         # Project examples
│   └── README.md               # Examples guide
│
├── mcp_service/                # MCP service (non-Claude fallback)
│   ├── server.py
│   └── docs/
│
├── marketplace.json            # Marketplace registry
└── README.md                   # This file
```

---

## Documentation

- **[Plugins Guide](plugins/README.md)** - How to use and create plugins
- **[Examples](examples/README.md)** - Example local contexts
- **[Sacred Seven](plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md)** - Core principles
- **[TDD Workflow](plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)** - Development process
- **[MCP Service](mcp_service/docs/)** - For non-Claude LLMs

---

## Migration from Old Version

If you were using the previous `example_projects_repo/` structure:

**Old**:
```
example_projects_repo/aisdlc_methodology/
contexts.json
```

**New**:
```
plugins/aisdlc-methodology/
marketplace.json
```

See [MIGRATION.md](MIGRATION.md) for complete guide.

---

## Benefits of This Approach

✅ **90% simpler** - Uses Claude Code's native plugin system instead of custom federation
✅ **Standard** - Follows Claude Code conventions
✅ **Federated** - Multiple marketplaces (corporate, division, local)
✅ **Composable** - Plugin loading order = merge priority
✅ **Portable** - Share via GitHub/Git marketplaces
✅ **Extensible** - Create your own plugins easily
✅ **Fallback** - MCP service for non-Claude LLMs

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT

---

## Acknowledgments

- Inspired by [ai_init](https://github.com/foolishimp/ai_init) - Original Sacred Seven methodology
- Built with Claude Code and the Sacred Seven principles
- Simplified dramatically by leveraging Claude Code's native marketplace system

**"Excellence or nothing"** 🔥
