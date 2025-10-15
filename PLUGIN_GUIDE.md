# AI_SDLC_Context Claude Code Plugin

## What's New: Plugin Version!

AI_SDLC_Context is now a **Claude Code Plugin** that can be installed with a single command!

### Plugin vs MCP Server

**Before (MCP Server Only):**
- Manual configuration in `claude_desktop_config.json`
- Use MCP tools via Claude Desktop
- Requires restart to load

**Now (Full Plugin):**
- Install with `/plugin` command
- Custom slash commands (`/load-context`, `/apply-persona`)
- Auto-suggestions and hooks
- Works in Claude Code (CLI + VS Code)
- Easy team sharing

## Installation

### Quick Install

```bash
/plugin https://github.com/foolishimp/AI_SDLC_Context
```

That's it! The plugin will install:
- ✅ 9 slash commands
- ✅ 21 MCP tools
- ✅ Auto-behavior hooks
- ✅ Context and persona management

### Requirements

- Claude Code (terminal or VS Code)
- Python 3.11+
- `pip install pyyaml mcp`

## Quick Start

### 1. List Available Options

```bash
# See all project contexts
/list-projects

# See all personas
/list-personas
```

### 2. Load a Project Context

```bash
# Load payment gateway context
/load-context payment_gateway

# Claude now applies PCI compliance, 95% coverage, strict security
```

### 3. Apply a Persona

```bash
# Apply security engineer perspective
/apply-persona security_engineer

# Claude now focuses on vulnerabilities, compliance, encryption
```

### 4. Combined Usage

```bash
# Load project + persona
/load-context payment_gateway
/apply-persona security_engineer

# Result: Payment gateway requirements + security focus
```

## Available Commands

### Context Management (5 commands)

| Command | Description |
|---------|-------------|
| `/list-projects` | Show all available project contexts |
| `/load-context <project>` | Load a project context |
| `/switch-context <project>` | Switch to different context |
| `/current-context` | Show active context |
| `/show-full-context` | Display complete context state with all layers |

### Persona Management (4 commands)

| Command | Description |
|---------|-------------|
| `/list-personas` | Show all available personas |
| `/apply-persona <persona>` | Apply a role perspective |
| `/switch-persona <persona>` | Switch personas |
| `/persona-checklist` | Get review checklist |

## Auto-Behaviors (Hooks)

The plugin includes smart behaviors:

### On Session Start
- Shows quick start guide
- Lists available commands

### On File Open
- Detects payment-related files → Suggests `/load-context payment_gateway`
- Detects admin files → Suggests `/load-context admin_dashboard`

### Pre-Commit
- Reminds you to verify persona checklist
- Shows active context requirements

### On Code Review
- Reviewing tests? → Suggests `/apply-persona qa_engineer`
- Security code? → Suggests `/apply-persona security_engineer`
- Deployment files? → Suggests `/apply-persona devops_engineer`

## Example Workflows

### Workflow 1: Multi-Project Development

```bash
# Morning: Work on payment gateway
/load-context payment_gateway
/apply-persona software_engineer
# ... code with strict PCI compliance ...

# Afternoon: Switch to admin dashboard
/switch-context admin_dashboard
# ... code with relaxed requirements ...
```

### Workflow 2: Multi-Role Code Review

```bash
# Load project
/load-context payment_gateway

# Review 1: Engineer perspective
/apply-persona software_engineer
# ... check code quality, tests, SOLID principles ...

# Review 2: Security perspective
/switch-persona security_engineer
/persona-checklist
# ... check vulnerabilities, encryption, auth ...

# Review 3: DevOps perspective
/switch-persona devops_engineer
/persona-checklist
# ... check deployability, monitoring, rollback ...
```

### Workflow 3: Compliance Audit

```bash
# Set up for audit
/load-context payment_gateway
/apply-persona security_engineer

# Get checklist
/persona-checklist

# Audit code against checklist:
# □ Are there security vulnerabilities?
# □ Is authentication proper?
# □ Is data encrypted?
# □ Are inputs validated?
# □ Are secrets properly managed?
```

## 6 Available Personas

1. **business_analyst**
   - Focus: Requirements, user stories
   - Hides: Technical implementation details
   - Tools: JIRA, Confluence, Lucidchart

2. **software_engineer**
   - Focus: Code quality, TDD, SOLID
   - Coverage: 90% unit, 80% integration
   - Tools: VSCode, Git, pytest

3. **qa_engineer**
   - Focus: Test coverage, quality gates
   - Levels: 7 testing levels
   - Automation: 80% minimum

4. **data_architect**
   - Focus: Data modeling, schema
   - Standards: 3NF normalization
   - Artifacts: ERD, migrations

5. **security_engineer**
   - Focus: Vulnerabilities, compliance
   - Testing: SAST, DAST, penetration
   - SLA: 4-hour critical fixes

6. **devops_engineer**
   - Focus: CI/CD, infrastructure
   - Strategy: Blue-green deployments
   - Tools: Terraform, Kubernetes

## Toggle Plugin On/Off

```bash
# Disable plugin temporarily
/plugin disable AI_SDLC_Context

# Re-enable plugin
/plugin enable AI_SDLC_Context
```

## Comparison with MCP-Only

| Feature | MCP Server | Plugin |
|---------|------------|--------|
| Installation | Manual config | `/plugin` command |
| Commands | MCP tools | Slash commands |
| User Experience | "Use load_context tool" | `/load-context` |
| Auto-suggestions | ❌ No | ✅ Yes |
| Hooks | ❌ No | ✅ Yes |
| Team Sharing | Hard | Easy |
| Toggle On/Off | Restart needed | Command |

## MCP Server Still Available

The underlying MCP server with 20 tools is still available for Claude Desktop users who prefer that approach. See [MCP_SETUP.md](MCP_SETUP.md).

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Detailed examples
- [MCP_SETUP.md](MCP_SETUP.md) - MCP server setup
- [PERSONAS.md](mcp_service/docs/PERSONAS.md) - Persona system docs
- [CONTEXT_MANAGEMENT.md](mcp_service/docs/CONTEXT_MANAGEMENT.md) - Context system docs

## Support

- GitHub: https://github.com/foolishimp/AI_SDLC_Context
- Issues: https://github.com/foolishimp/AI_SDLC_Context/issues

---

**Install now:** `/plugin https://github.com/foolishimp/AI_SDLC_Context` 🚀
