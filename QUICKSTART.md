# AI_SDLC_Context Quick Start Guide

Get started with the **7-Stage AI SDLC Methodology** in 3 different ways:
1. Claude Code Plugin (recommended)
2. Direct Python usage (programmatic)
3. Through Claude Desktop (MCP)

## Table of Contents
- [What is AI_SDLC_Context?](#what-is-ai_sdlc_context)
- [Method 1: Claude Code Plugin (Recommended)](#method-1-claude-code-plugin-recommended)
- [Method 2: Direct Python Usage](#method-2-direct-python-usage)
- [Method 3: MCP with Claude Desktop](#method-3-mcp-with-claude-desktop)
- [Common Use Cases](#common-use-cases)

---

## What is AI_SDLC_Context?

AI_SDLC_Context is an **Intent-Driven AI SDLC Methodology** providing:

### 7-Stage Software Development Lifecycle

```
Intent → Requirements → Design → Tasks → Code → System Test → UAT → Runtime Feedback
           ↑                                                                    ↓
           └────────────────────── Feedback Loop ──────────────────────────────┘
```

**Complete Lifecycle**:
1. **Requirements** - Transform intent into structured requirements (REQ-F-*, REQ-NFR-*, REQ-DATA-*)
2. **Design** - Create technical solution architecture (components, APIs, data models)
3. **Tasks** - Break down into work units with Jira orchestration
4. **Code** - TDD implementation (RED → GREEN → REFACTOR) + Key Principles principles
5. **System Test** - BDD integration testing (Given/When/Then scenarios)
6. **UAT** - Business validation and sign-off
7. **Runtime Feedback** - Production telemetry closes the loop back to requirements

### Key Features

✅ **Requirement Traceability** - Track requirement keys from intent to runtime
✅ **AI Agent Configurations** - Detailed specs for AI agents at each SDLC stage
✅ **Bidirectional Feedback** - Production issues flow back to requirements
✅ **Key Principles Principles** - Foundation for Code stage (TDD, Fail Fast, etc.)
✅ **Claude Code Plugins** - Installable methodology and standards
✅ **Federated Architecture** - Compose contexts across corporate → division → team → project

---

## Method 1: Claude Code Plugin (Recommended)

### Installation

```bash
# In Claude Code (CLI or VS Code)
/plugin marketplace add foolishimp/AI_SDLC_Context
/plugin install @aisdlc/aisdlc-methodology
```

### Quick Start Example

```bash
# See available projects
/plugin install @aisdlc/aisdlc-methodology

# Claude now has access to:
# - Complete 7-stage AI SDLC methodology
# - AI agent configurations for each stage
# - Key Principles principles
# - TDD workflow (RED → GREEN → REFACTOR)
# - BDD testing guides
# - Requirement traceability system
```

### Example: Customer Portal Development

Create a project using the 7-stage methodology:

**Your `.claude/settings.json`:**
```json
{
  "plugins": [
    "@aisdlc/aisdlc-methodology",
    "@aisdlc/python-standards"
  ]
}
```

**Your project's `config.yml`:**
```yaml
ai_sdlc:
  methodology_plugin: "file://plugins/aisdlc-methodology/config/stages_config.yml"

  enabled_stages:
    - requirements    # Intent → Structured requirements
    - design          # Requirements → Technical solution
    - tasks           # Work breakdown + Jira
    - code            # TDD (RED → GREEN → REFACTOR)
    - system_test     # BDD integration testing
    - uat             # Business validation
    - runtime_feedback # Production telemetry feedback

  stages:
    code:
      testing:
        coverage_minimum: 90
      key.principles:
        enabled: true
```

**Ask Claude:**
```
"Help me implement the authentication feature following the AI SDLC methodology"

Claude will:
1. Generate requirements (REQ-F-AUTH-001, etc.)
2. Create design artifacts (component diagrams, APIs)
3. Break into tasks (Jira tickets with REQ tags)
4. Implement using TDD (RED → GREEN → REFACTOR)
5. Generate BDD tests (Given/When/Then)
6. Create UAT scenarios
7. Set up runtime telemetry with REQ key tagging
```

### See Complete Example

👉 **[examples/local_projects/customer_portal/](examples/local_projects/customer_portal/)** - Complete 7-stage walkthrough (800+ lines)

---

## Method 2: Direct Python Usage

For programmatic access or custom integrations:

```bash
# Clone repository
git clone https://github.com/foolishimp/AI_SDLC_Context.git
cd AI_SDLC_Context

# Install dependencies
pip install pyyaml
```

### Example: Load and Use Methodology

```python
from pathlib import Path
import yaml

# Load the 7-stage methodology configuration
stages_config_path = Path("plugins/aisdlc-methodology/config/stages_config.yml")
with open(stages_config_path) as f:
    methodology = yaml.safe_load(f)

# Access stage specifications
requirements_stage = methodology['ai_sdlc']['stages']['requirements']
code_stage = methodology['ai_sdlc']['stages']['code']

# Get agent configuration for Requirements stage
requirements_agent = requirements_stage['agent']
print(f"Role: {requirements_agent['role']}")
print(f"Purpose: {requirements_agent['purpose']}")

# Get Key Principles principles for Code stage
key.principles = code_stage['key.principles']
print(f"TDD Workflow: {key.principles['tdd']['workflow']}")
```

### Run Examples

```bash
# See all 7 stages in action
python examples/local_projects/customer_portal/walkthrough.py
```

---

## Method 3: MCP with Claude Desktop

For Claude Desktop users, the MCP service provides 7-stage AI SDLC support.

### Quick Setup

See [mcp_service/README.md](mcp_service/README.md) and [mcp_service/MCP_SDLC_INTEGRATION_PLAN.md](mcp_service/MCP_SDLC_INTEGRATION_PLAN.md) for complete instructions.

**Summary:**
1. `pip install mcp pyyaml`
2. Configure `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Restart Claude Desktop
4. Ask Claude: "What MCP tools are available?"

### Using MCP Tools (Planned)

**Example Conversation:**

```
You: "Load the customer_portal project for the Requirements stage"
Claude: [uses load_stage_context]
        Loads Requirements Agent configuration with requirement types

You: "Generate requirements for user authentication feature"
Claude: [uses Requirements Agent spec]
        Generates:
        - REQ-F-AUTH-001: "User login with email/password"
        - REQ-NFR-PERF-001: "Login response < 500ms"
        - REQ-DATA-001: "Email must be valid format"

You: "Switch to Code stage"
Claude: [uses load_stage_context with stage="code"]
        Loads Code Agent with Key Principles principles + TDD workflow

You: "Implement REQ-F-AUTH-001"
Claude: [uses Code Agent spec]
        Follows TDD workflow:
        1. RED: Write failing test_user_login()
        2. GREEN: Implement login() to pass
        3. REFACTOR: Clean up code
        4. Tag code with # Implements: REQ-F-AUTH-001
```

**Note**: Full MCP integration for 7-stage methodology is in progress. See [mcp_service/MCP_SDLC_INTEGRATION_PLAN.md](mcp_service/MCP_SDLC_INTEGRATION_PLAN.md) for details.

---

## Common Use Cases

### Use Case 1: Full Lifecycle Development

**Scenario:** Develop a feature from intent to production with complete traceability.

**With Claude Code Plugin:**
```bash
# Install methodology
/plugin install @aisdlc/aisdlc-methodology

# Ask Claude to follow 7-stage process
"Implement customer authentication feature using AI SDLC methodology"

Claude guides you through:
1. Requirements: Generate REQ-F-AUTH-001, REQ-NFR-PERF-001, etc.
2. Design: Create AuthenticationService component, API specs
3. Tasks: Break into JIRA tickets (PORTAL-123, PORTAL-124)
4. Code: TDD implementation with requirement tags
5. System Test: BDD scenarios (Given/When/Then)
6. UAT: Business validation test cases
7. Runtime Feedback: Setup telemetry with REQ key tagging

Result: Complete traceability from intent to production
```

### Use Case 2: Code Stage Only (TDD Focus)

**Scenario:** You already have requirements and design, just need implementation.

**With Claude Code Plugin:**
```yaml
# config.yml - Enable only Code stage
ai_sdlc:
  enabled_stages:
    - code  # TDD implementation only

  stages:
    code:
      key.principles:
        enabled: true
      tdd:
        workflow: "RED → GREEN → REFACTOR"
      testing:
        coverage_minimum: 80
```

Claude will:
- Follow TDD workflow strictly
- Apply Key Principles principles
- Ensure 80%+ test coverage
- Tag code with requirement keys

### Use Case 3: Multi-Stage Review

**Scenario:** Review code across different SDLC perspectives.

**Ask Claude:**
```
"Review this authentication code from Requirements, Code, and System Test perspectives"

Claude reviews:
1. Requirements Stage: Does code satisfy REQ-F-AUTH-001?
2. Code Stage: Does code follow TDD and Key Principles principles?
3. System Test Stage: Are there BDD scenarios validating the requirements?
```

### Use Case 4: Runtime Issue → New Intent

**Scenario:** Production alert triggers feedback loop to requirements.

**With Runtime Feedback Stage:**
```
Alert: "ERROR: REQ-F-AUTH-001 - Auth timeout in production"

Claude (Runtime Feedback Agent):
1. Traces REQ-F-AUTH-001 back through stages
2. Identifies root cause (performance requirement violated)
3. Generates new intent: INT-042 "Fix auth timeout"
4. Links to original requirement REQ-F-AUTH-001

New cycle begins at Requirements stage
```

---

## 7-Stage Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    INTENT MANAGER                           │
│  "Users need self-service portal with authentication"       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. REQUIREMENTS STAGE                                      │
│     • Transform intent → structured requirements            │
│     • Output: REQ-F-AUTH-001, REQ-NFR-PERF-001, etc.       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. DESIGN STAGE                                            │
│     • Requirements → technical solution                     │
│     • Output: AuthenticationService, API specs, data models │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. TASKS STAGE                                             │
│     • Design → work units                                   │
│     • Output: Jira tickets (PORTAL-123) tagged with REQ-*  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. CODE STAGE                                              │
│     • TDD: RED → GREEN → REFACTOR                          │
│     • Key Principles principles                               │
│     • Output: auth_service.py # Implements: REQ-F-AUTH-001 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  5. SYSTEM TEST STAGE                                       │
│     • BDD: Given/When/Then scenarios                        │
│     • Output: auth.feature validating REQ-F-AUTH-001       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  6. UAT STAGE                                               │
│     • Business validation                                   │
│     • Output: UAT-001 → REQ-F-AUTH-001 (Business sign-off) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  7. RUNTIME FEEDBACK STAGE                                  │
│     • Telemetry: Tagged with REQ-F-AUTH-001                │
│     • Alerts → New intents (feedback loop)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         └──────────► Back to Intent Manager
```

---

## Documentation

### Core Methodology
- [docs/ai_sdlc_guide.md](docs/ai_sdlc_guide.md) - Complete 7-stage methodology (3,300+ lines) ⭐ **Start here**
- [docs/README.md](docs/README.md) - Documentation index with role-based learning paths

### Plugin Documentation
- [plugins/README.md](plugins/README.md) - Plugin creation and usage guide
- [plugins/aisdlc-methodology/README.md](plugins/aisdlc-methodology/README.md) - Methodology plugin docs

### Examples
- [examples/local_projects/customer_portal/README.md](examples/local_projects/customer_portal/README.md) - Complete 7-stage walkthrough (800+ lines)
- [examples/README.md](examples/README.md) - All examples overview

### MCP Service (Non-Claude LLMs)
- [mcp_service/README.md](mcp_service/README.md) - MCP service overview
- [mcp_service/MCP_SDLC_INTEGRATION_PLAN.md](mcp_service/MCP_SDLC_INTEGRATION_PLAN.md) - 7-stage integration roadmap

---

## Next Steps

### For New Users

1. **Read the methodology**: [docs/ai_sdlc_guide.md](docs/ai_sdlc_guide.md)
2. **Review the example**: [examples/local_projects/customer_portal/](examples/local_projects/customer_portal/)
3. **Install the plugin**: `/plugin install @aisdlc/aisdlc-methodology`
4. **Start developing**: Ask Claude to follow the 7-stage AI SDLC methodology

### For Role-Specific Learning

See [docs/README.md](docs/README.md) for learning paths tailored to:
- Business Analysts / Product Owners
- Architects / Technical Leads
- Developers
- QA Engineers
- DevOps / SRE
- Project Managers / Scrum Masters

---

**"Excellence or nothing"** 🔥

**Ready to start!** Install the plugin or review the examples. 🚀
