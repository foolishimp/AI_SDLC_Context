# AI_SDLC_Context

**Intent-Driven AI SDLC Methodology** with full requirement traceability and 7-stage agent orchestration.

**Mantra**: **"Excellence or nothing"** 🔥

---

## What Is This?

A complete **AI-Augmented Software Development Lifecycle (AI SDLC)** framework providing:

- **🎯 7-Stage Methodology**: Requirements → Design → Tasks → Code → System Test → UAT → Runtime Feedback
- **🔗 Requirement Traceability**: Track requirement keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*) from intent to runtime
- **🤖 AI Agent Configurations**: Detailed specifications for AI agents at each SDLC stage
- **📦 Claude Code Plugins**: Installable methodology and standards as plugins
- **🏢 Federated Architecture**: Compose contexts across corporate → division → team → project
- **🔄 Bidirectional Feedback**: Production issues flow back to requirements and generate new intents

### The 7-Stage AI SDLC

```
Intent → Requirements → Design → Tasks → Code → System Test → UAT → Runtime Feedback
   ↑                                                                         ↓
   └─────────────────────────── Feedback Loop ───────────────────────────────┘
```

Each stage has:
- **AI Agent specification** with clear responsibilities
- **Quality gates** for stage completion
- **Traceability** to requirement keys
- **Personas** (human roles and AI agents)

👉 **Full Methodology**: [AI SDLC Guide](docs/ai_sdlc_guide.md)
👉 **Example Project**: [customer_portal](examples/local_projects/customer_portal/)

---

## Quick Start

### Option 1: Use Claude Code Plugins (Recommended)

#### 1. Add This Marketplace

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

#### 2. Install AI SDLC Methodology Plugin

```bash
/plugin install @aisdlc/aisdlc-methodology
```

**What you get**:
- Complete 7-stage AI SDLC workflow
- Sacred Seven development principles
- TDD workflow (RED → GREEN → REFACTOR)
- BDD testing guidelines
- Requirement traceability framework

#### 3. Optional: Install Language Standards

```bash
/plugin install @aisdlc/python-standards
```

#### 4. Start Using the Methodology!

Claude will now follow the 7-stage AI SDLC methodology automatically.

### Option 2: Explore the Methodology First

```bash
# Clone the repository
git clone https://github.com/foolishimp/AI_SDLC_Context.git
cd AI_SDLC_Context

# Read the complete methodology guide
open docs/ai_sdlc_guide.md

# Explore the example project (7-stage workflow)
open examples/local_projects/customer_portal/README.md

# Review the methodology plugin
open plugins/aisdlc-methodology/README.md
```

---

## The 7 Stages Explained

### 1. Requirements Stage (Section 4.0)
**Agent**: Requirements Agent
**Purpose**: Transform intent into structured requirements with unique, immutable keys

**Outputs**: REQ-F-* (functional), REQ-NFR-* (non-functional), REQ-DATA-* (data quality), REQ-BR-* (business rules)

### 2. Design Stage (Section 5.0)
**Agent**: Design Agent / Solution Designer
**Purpose**: Transform requirements into implementable technical and data solution

**Outputs**: Component diagrams, data models, API specifications, architecture decision records (ADRs)

### 3. Tasks Stage (Section 6.0)
**Agent**: Tasks Stage Orchestrator
**Purpose**: Work breakdown with Jira integration and agent orchestration

**Outputs**: Jira epics/stories with requirement tags, dependency graph, capacity planning

### 4. Code Stage (Section 7.0)
**Agent**: Code Agent / Developer Agent
**Purpose**: TDD-driven implementation (RED → GREEN → REFACTOR)

**Methodology**: Sacred Seven principles + TDD cycle
**Outputs**: Production code with requirement tags, unit tests, integration tests

### 5. System Test Stage (Section 8.0)
**Agent**: System Test Agent / QA Agent
**Purpose**: BDD integration testing (Given/When/Then)

**Outputs**: BDD feature files (Gherkin), step definitions, coverage matrix (≥95% requirement coverage)

### 6. UAT Stage (Section 9.0)
**Agent**: UAT Agent
**Purpose**: Business validation with BDD in pure business language

**Outputs**: Manual UAT test cases, automated UAT tests, business sign-off

### 7. Runtime Feedback Stage (Section 10.0)
**Agent**: Runtime Feedback Agent
**Purpose**: Production telemetry and feedback loop closure

**Outputs**: Release manifests with requirement traceability, runtime alerts linked to requirement keys, new intents from production issues

👉 **Detailed Specifications**: [AI SDLC Guide](docs/ai_sdlc_guide.md)

---

## Requirement Traceability Example

```
Intent: INT-001 "Customer self-service portal"
  ↓
Requirements: REQ-F-AUTH-001 "User login with email/password"
  ↓
Design: AuthenticationService → REQ-F-AUTH-001
  ↓
Tasks: PORTAL-123 (Jira ticket) → REQ-F-AUTH-001
  ↓
Code: auth_service.py
      # Implements: REQ-F-AUTH-001
  ↓
Tests: test_auth.py # Validates: REQ-F-AUTH-001
       auth.feature # BDD: Given/When/Then for REQ-F-AUTH-001
  ↓
UAT: UAT-001 → REQ-F-AUTH-001 (Business sign-off ✅)
  ↓
Runtime: Datadog alert: "ERROR: REQ-F-AUTH-001 - Auth timeout"
  ↓
Feedback: New intent: INT-042 "Fix auth timeout"
  [Cycle repeats...]
```

**Every artifact tagged with requirement keys** for complete traceability!

---

## Sacred Seven Principles (Code Stage Foundation)

The Code Stage (Section 7.0) is built on these principles:

1. **Test Driven Development** - "No code without tests"
   - TDD cycle: RED → GREEN → REFACTOR → COMMIT
   - Minimum 80% coverage (critical paths 100%)

2. **Fail Fast & Root Cause** - "Break loudly, fix completely"
   - No workarounds or band-aids
   - Tests fail loudly, fix root causes

3. **Modular & Maintainable** - "Single responsibility, loose coupling"
   - Each module does one thing well
   - Clean, understandable code

4. **Reuse Before Build** - "Check first, create second"
   - Search existing code first
   - Avoid duplication

5. **Open Source First** - "Suggest alternatives, human decides"
   - AI suggests options
   - Humans make final decisions

6. **No Legacy Baggage** - "Clean slate, no debt"
   - No technical debt
   - Clean implementation

7. **Perfectionist Excellence** - "Best of breed only"
   - Quality over quantity
   - Excellence or nothing

👉 **Full Principles**: [Sacred Seven](plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md)

---

## Available Plugins

### aisdlc-methodology v2.0.0

**Core AI SDLC methodology** - Complete 7-stage workflow

**Provides**:
- ✅ Complete 7-stage AI SDLC agent configurations
- ✅ Sacred Seven development principles
- ✅ TDD workflow (RED → GREEN → REFACTOR)
- ✅ BDD testing guidelines (Given/When/Then)
- ✅ Requirement traceability framework
- ✅ Quality gates for each stage
- ✅ Persona specifications (human roles + AI agents)
- ✅ Pair programming practices
- ✅ Session management guides

**Reference**: [docs/ai_sdlc_guide.md](docs/ai_sdlc_guide.md)
**Dependencies**: None (foundation)

👉 [Full Documentation](plugins/aisdlc-methodology/README.md)

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
    "@corporate/aisdlc-methodology",      // Corporate baseline (7 stages)
    "@corporate/python-standards",         // Corporate Python standards
    "@division/backend-standards",         // Division overrides
    "@local/my-team-customizations",       // Team customizations
    "@local/my-project-context"            // Project-specific
  ]
}
```

**Plugin loading order** = merge priority. Later plugins override earlier ones.

---

## Example Projects

### customer_portal (⭐ Complete 7-Stage Example)

**Purpose**: Demonstrates complete 7-stage AI SDLC with full requirement traceability

**Shows**:
- All 7 stages in action
- Requirement key propagation (REQ-F-AUTH-001 flows through all stages)
- TDD workflow in Code stage
- BDD testing in System Test and UAT stages
- Runtime feedback creating new intents
- Complete bidirectional traceability

👉 [Detailed Walkthrough](examples/local_projects/customer_portal/README.md)

### api_platform

**Purpose**: Public API with backwards compatibility requirements

**Shows**: How to override Principle #6 (No Legacy Baggage) for customer-facing APIs using feature flags

👉 [API Platform Example](examples/local_projects/api_platform/README.md)

### More Examples

See [examples/README.md](examples/README.md) for complete list

---

## Creating Your Own Project with AI SDLC

See [plugins/README.md](plugins/README.md) for complete guide.

### Quick Example

```bash
# Create project structure
mkdir -p my-project/.claude-plugin
cd my-project

# Create plugin.json
cat > .claude-plugin/plugin.json <<EOF
{
  "name": "my-project-context",
  "version": "1.0.0",
  "displayName": "My Project",
  "dependencies": {
    "aisdlc-methodology": "^2.0.0",
    "python-standards": "^1.0.0"
  }
}
EOF

# Create project config with 7-stage SDLC
mkdir config
cat > config/context.yml <<EOF
project:
  name: "my-payment-api"
  risk_level: "high"

# Reference 7-stage methodology plugin
ai_sdlc:
  methodology_plugin: "file://../../plugins/aisdlc-methodology/config/stages_config.yml"

  # Enable stages you need
  enabled_stages:
    - requirements
    - design
    - tasks
    - code
    - system_test
    - uat
    - runtime_feedback

  # Project-specific quality standards
  stages:
    code:
      testing:
        coverage_minimum: 95  # Override baseline 80%

    system_test:
      requirement_coverage_minimum: 98  # Override baseline 95%

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
├── aisdlc-methodology/        # 7-stage AI SDLC
├── python-standards/
├── javascript-standards/
├── security-baseline/
└── compliance-requirements/
```

All developers add this marketplace and get company standards + 7-stage methodology.

### Division Customizations

Engineering division extends corporate with specific practices:

```
division-marketplace/
├── backend-api-standards/      # Extends python-standards
├── frontend-standards/          # Extends javascript-standards
├── microservices-patterns/
└── division-sdlc-overrides/    # Stage-specific customizations
```

### Team/Project Contexts

Individual teams create local contexts:

```
.claude-plugins/
├── team-conventions/
└── project-specific/
    └── config/
        └── context.yml         # Project-specific 7-stage config
```

### Result: Layered Composition

```
Corporate (baseline + 7-stage SDLC)
  └─> Division (extensions + stage customizations)
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

**MCP Service Features**:
- Project CRUD operations
- Stage-specific context loading
- Requirement traceability tracking
- AI agent orchestration
- Persona management (human + AI agents)

See [mcp_service/docs/](mcp_service/docs/) and [MCP Integration Plan](mcp_service/MCP_SDLC_INTEGRATION_PLAN.md) for details.

**For Claude Code users**: Just use the marketplace approach (simpler!).

---

## Project Structure

```
AI_SDLC_Context/
├── docs/
│   ├── ai_sdlc_guide.md             # ⭐ Complete 7-stage methodology (3,300+ lines)
│   └── README.md                     # Documentation index
│
├── plugins/                          # Claude Code plugins
│   ├── aisdlc-methodology/          # 7-stage AI SDLC v2.0.0
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Plugin metadata (7 stages)
│   │   ├── config/
│   │   │   ├── stages_config.yml    # Complete 7-stage agent specs (1,273 lines)
│   │   │   └── config.yml           # Sacred Seven + TDD workflow
│   │   ├── docs/                    # Methodology documentation
│   │   └── README.md                # Plugin overview
│   │
│   ├── python-standards/            # Python standards plugin
│   └── README.md                    # Plugin creation guide
│
├── examples/                         # Example projects
│   ├── local_projects/
│   │   ├── customer_portal/         # ⭐ Complete 7-stage example
│   │   ├── api_platform/            # Public API example
│   │   ├── payment_gateway/         # High-risk project
│   │   └── admin_dashboard/         # Low-risk project
│   └── README.md                    # Examples guide
│
├── mcp_service/                     # MCP service (non-Claude fallback)
│   ├── server/
│   ├── docs/
│   ├── MCP_SDLC_INTEGRATION_PLAN.md # 7-stage integration roadmap
│   └── README.md
│
├── marketplace.json                 # Claude Code marketplace registry
└── README.md                        # This file
```

---

## Documentation

### Core Methodology
- **[AI SDLC Guide](docs/ai_sdlc_guide.md)** ⭐ - Complete 7-stage methodology (3,300+ lines)
- **[7-Stage Example](examples/local_projects/customer_portal/README.md)** - Full walkthrough
- **[Methodology Plugin](plugins/aisdlc-methodology/README.md)** - Plugin overview

### Principles & Processes
- **[Sacred Seven Principles](plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md)** - Core principles
- **[TDD Workflow](plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)** - Development process
- **[Pair Programming](plugins/aisdlc-methodology/docs/guides/PAIR_PROGRAMMING_WITH_AI.md)** - Human-AI collaboration

### Guides
- **[Plugins Guide](plugins/README.md)** - How to use and create plugins
- **[Examples Guide](examples/README.md)** - Example local contexts
- **[MCP Service](mcp_service/README.md)** - For non-Claude LLMs
- **[MCP Integration Plan](mcp_service/MCP_SDLC_INTEGRATION_PLAN.md)** - 7-stage integration roadmap

---

## Benefits of This Approach

### Methodology Benefits
✅ **Complete Lifecycle Coverage** - 7 stages from Intent to Runtime Feedback
✅ **End-to-End Traceability** - Requirement keys flow through entire pipeline
✅ **AI Agent Ready** - Detailed specifications for each stage agent
✅ **Feedback-Driven** - Continuous improvement through closed loops
✅ **Concurrent Execution** - Support for parallel sub-vector SDLCs
✅ **Context-Driven** - Standards and templates guide all stages
✅ **Quality Gates** - Clear pass/fail criteria at each stage

### Technical Benefits
✅ **90% simpler** - Uses Claude Code's native plugin system
✅ **Standard** - Follows Claude Code conventions
✅ **Federated** - Multiple marketplaces (corporate, division, local)
✅ **Composable** - Plugin loading order = merge priority
✅ **Portable** - Share via GitHub/Git marketplaces
✅ **Extensible** - Create your own plugins easily
✅ **Fallback** - MCP service for non-Claude LLMs

---

## Migration from Old Version

If you were using the previous `example_projects_repo/` structure:

**Old**:
```
example_projects_repo/aisdlc_methodology/  (v1.0 - Code stage only)
contexts.json
```

**New**:
```
plugins/aisdlc-methodology/  (v2.0 - Complete 7-stage SDLC)
marketplace.json
```

See [MIGRATION.md](MIGRATION.md) for complete guide.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT

---

## Acknowledgments

- **Inspired by** [ai_init](https://github.com/foolishimp/ai_init) - Original Sacred Seven methodology
- **Expanded with** Complete 7-stage AI SDLC framework
- **Built with** Claude Code and the Sacred Seven principles
- **Simplified** by leveraging Claude Code's native marketplace system

---

## Version History

### v2.0.0 (2025-11-14) - 7-Stage AI SDLC
- ✨ Added complete 7-stage AI SDLC methodology
- ✨ Added requirement traceability framework (REQ-* keys)
- ✨ Added AI agent specifications for each stage
- ✨ Added BDD testing guidelines (System Test & UAT stages)
- ✨ Added Runtime Feedback stage with observability integration
- ✨ Added complete example project (customer_portal)
- ✨ Added comprehensive methodology guide (3,300+ lines)
- ✨ Added MCP service integration plan

### v1.0.0 (2025-10-17) - Initial Release
- Initial release with Sacred Seven principles
- TDD workflow for Code stage
- Claude Code plugin marketplace

---

**"Excellence or nothing"** 🔥
