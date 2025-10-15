# AI_SDLC_config Quick Start Guide

This guide shows you how to use the AI_SDLC_config system in 3 different ways:
1. Direct Python usage (programmatic)
2. Command-line examples
3. Through Claude Desktop (MCP)

## Table of Contents
- [What is AI_SDLC_config?](#what-is-ai_sdlc_config)
- [Installation](#installation)
- [Method 1: Direct Python Usage](#method-1-direct-python-usage)
- [Method 2: MCP with Claude Desktop](#method-2-mcp-with-claude-desktop)
- [Method 3: Examples and Demos](#method-3-examples-and-demos)
- [Common Use Cases](#common-use-cases)

---

## What is AI_SDLC_config?

AI_SDLC_config is a **5-layer hierarchical configuration management system** that enables:

1. **Dynamic Context Switching** - Claude adapts to different project requirements
2. **Persona-Based Views** - Same project, different perspectives (BA, Engineer, QA, etc.)
3. **Priority-Based Merging** - Configurations merge with clear precedence
4. **Git-Backed Storage** - Full audit trail of all changes

### The 5 Layers (Lowest to Highest Priority)

```
5. Persona         ← Highest Priority (role-based overrides)
4. Runtime         ← Environment-specific (dev, staging, prod)
3. Project         ← Project-specific requirements
2. Methodology     ← Language/framework standards
1. Corporate Base  ← Lowest Priority (company defaults)
```

---

## Installation

### Prerequisites

```bash
# Python 3.11+
python --version

# Install dependencies
pip install pyyaml
pip install mcp  # Only needed for Claude Desktop integration
```

### Clone the Repository

```bash
cd ~/src/apps
git clone https://github.com/foolishimp/AI_SDLC_config.git
cd AI_SDLC_config
```

---

## Method 1: Direct Python Usage

Run the included examples to see the system in action:

```bash
# Basic project operations (CRUD, merge, git audit)
python mcp_service/examples/direct_usage_example.py

# Context management (load, switch, query)
python mcp_service/examples/context_management_demo.py

# Persona system (6 roles viewing same project)
python mcp_service/examples/persona_demo.py
```

---

## Method 2: MCP with Claude Desktop

### Quick Setup

See [MCP_SETUP.md](MCP_SETUP.md) for complete instructions.

**Summary:**
1. `pip install mcp`
2. Configure `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Restart Claude Desktop
4. Ask Claude: "What MCP tools are available?"

### Using MCP Tools

**Example Conversation:**

```
You: "List the available personas"
Claude: [uses list_personas]
        Shows 6 personas with focus areas

You: "Load the payment_gateway context"
Claude: [uses load_context]
        Loads PCI-compliant payment gateway requirements

You: "Apply the security_engineer persona"
Claude: [uses apply_persona_to_context]
        Views project through security lens

You: "What should I review?"
Claude: [uses get_persona_checklist]
        Shows security review checklist
```

---

## Method 3: Examples and Demos

### Available Demos

```bash
cd /Users/jim/src/apps/AI_SDLC_config

# 1. Direct usage example
python mcp_service/examples/direct_usage_example.py

# 2. Context management
python mcp_service/examples/context_management_demo.py

# 3. Persona demonstration
python mcp_service/examples/persona_demo.py

# 4. Validate MCP tools
python mcp_service/examples/validate_tools.py
```

### What Each Demo Shows

**direct_usage_example.py:**
- Create projects (base, methodology, custom)
- Update configurations
- Add documentation
- Merge projects
- Git audit trail

**context_management_demo.py:**
- Load project contexts
- Switch between contexts
- Detect requirement changes
- Context-aware formatting

**persona_demo.py:**
- All 6 personas viewing same project
- Different focus areas per persona
- Role-specific review checklists
- Persona switching with diff

---

## Common Use Cases

### Use Case 1: Multi-Project Development

**Scenario:** Working on multiple projects with different requirements.

**With MCP (Claude Desktop):**
```
"Load the payment_gateway context"
→ Claude generates PCI-compliant code with fraud detection

"Switch to admin_dashboard context"
→ Claude generates simpler code without heavy security
```

### Use Case 2: Team Collaboration

**Scenario:** Different team members review code from different perspectives.

**With MCP:**
```
"Apply the qa_engineer persona"
→ Checklist focuses on testing, automation, quality gates

"Switch to security_engineer persona"
→ Checklist focuses on vulnerabilities, encryption, compliance
```

### Use Case 3: Code Review

**Scenario:** Need role-specific review checklist.

**With MCP:**
```
"Apply the devops_engineer persona and get the review checklist"
→ □ Is this deployable?
  □ Are there deployment scripts?
  □ Is rollback possible?
  □ Are there monitoring hooks?
```

---

## Available Tools

### 20 MCP Tools

**Project Management (11):**
- create_project, get_project, list_projects
- update_project, delete_project
- add_node, remove_node, add_document
- merge_projects, inspect_project, compare_projects

**Context Management (4):**
- load_context, switch_context
- query_context, get_current_context

**Persona Management (5):**
- list_personas, load_persona
- apply_persona_to_context, switch_persona
- get_persona_checklist

---

## 6 Available Personas

1. **business_analyst** - Requirements & business logic (hides technical details)
2. **software_engineer** - Code quality & TDD (90% unit coverage)
3. **qa_engineer** - Test coverage (7 testing levels, 80% automation)
4. **data_architect** - Data modeling (3NF, ERD diagrams)
5. **security_engineer** - Security & compliance (4-hour critical SLA)
6. **devops_engineer** - CI/CD & infrastructure (blue-green deployments)

---

## Quick Example: End-to-End

```bash
# 1. Run the persona demo to see the system in action
python mcp_service/examples/persona_demo.py

# 2. Set up Claude Desktop (one time)
# See MCP_SETUP.md

# 3. In Claude Desktop, try:
"List the available personas"
"Load the payment_gateway context"
"Apply the security_engineer persona"
"Get the review checklist"
```

---

## Documentation

- [README.md](README.md) - Project overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed design
- [MCP_SETUP.md](MCP_SETUP.md) - Claude Desktop setup guide
- [CONTEXT_MANAGEMENT.md](mcp_service/docs/CONTEXT_MANAGEMENT.md) - Context system docs
- [PERSONAS.md](mcp_service/docs/PERSONAS.md) - Persona system docs

---

**Ready to start!** Run the demos or set up Claude Desktop integration. 🚀
