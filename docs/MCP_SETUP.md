# MCP Server Setup for Claude Desktop

This guide shows how to use the AI_SDLC_Context MCP server with Claude Desktop for dynamic context and persona management.

## What This Enables

The MCP server provides **20 tools** that allow Claude to:

1. **Manage Projects** (11 tools)
   - Create, read, update, delete configuration projects
   - Merge multiple projects with priority-based overrides
   - Add documentation and configuration nodes

2. **Switch Contexts Dynamically** (4 tools)
   - Load different project contexts (payment_gateway, admin_dashboard, etc.)
   - Switch between contexts mid-conversation
   - Query current context for requirements

3. **Apply Personas** (5 tools)
   - View projects through different role lenses
   - 6 pre-defined personas: Business Analyst, Software Engineer, QA Engineer, Data Architect, Security Engineer, DevOps Engineer
   - Get role-specific review checklists

## Installation

### 1. Install MCP SDK (if not already installed)

```bash
pip install mcp
```

### 2. Configure Claude Desktop

The configuration is already set up at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Current configuration:
```json
{
  "mcpServers": {
    "ai-sdlc-config": {
      "command": "python",
      "args": [
        "/Users/jim/src/apps/AI_SDLC_Context/mcp_service/server/main.py",
        "--repo-path",
        "/Users/jim/src/apps/AI_SDLC_Context/projects_repo",
        "--personas-path",
        "/Users/jim/src/apps/AI_SDLC_Context/personas"
      ]
    }
  }
}
```

### 3. Restart Claude Desktop

**IMPORTANT**: You must restart Claude Desktop for the MCP server to be loaded.

1. Quit Claude Desktop completely (Cmd+Q)
2. Relaunch Claude Desktop
3. Look for the 🔌 icon or MCP indicator showing the server is connected

## Using the MCP Tools

### Example 1: List Available Projects

Ask Claude:
> "Use the list_projects tool to show me what configuration projects are available"

### Example 2: Load a Project Context

Ask Claude:
> "Load the payment_gateway context using load_context"

Claude will see all the requirements for the payment gateway project (PCI compliance, fraud detection, etc.)

### Example 3: Apply a Persona

Ask Claude:
> "List the available personas, then apply the security_engineer persona to the current context"

Now Claude will view the project through a security engineer's lens:
- Zero-tolerance for vulnerabilities
- Focus on SAST/DAST testing
- 4-hour critical fix SLA
- Security review checklist

### Example 4: Switch Contexts

Ask Claude:
> "Switch from payment_gateway to admin_dashboard context"

Claude will detect what requirements changed and adapt its behavior.

### Example 5: Get Persona Checklist

Ask Claude:
> "Get the review checklist for the qa_engineer persona"

Claude will show the QA-specific code review checklist.

## Available MCP Tools

### Project Management (11 tools)
- `create_project` - Create a new configuration project
- `get_project` - Get project metadata
- `list_projects` - List all projects
- `update_project` - Update project configuration
- `delete_project` - Delete a project
- `add_node` - Add a configuration node
- `remove_node` - Remove a configuration node
- `add_document` - Add documentation file
- `merge_projects` - Merge multiple projects
- `inspect_project` - Query project with natural language
- `compare_projects` - Compare two projects

### Context Management (4 tools)
- `load_context` - Load a project context
- `switch_context` - Switch to different context
- `query_context` - Query current context
- `get_current_context` - Get current context info

### Persona Management (5 tools)
- `list_personas` - List available personas
- `load_persona` - Load a persona
- `apply_persona_to_context` - Apply persona to context
- `switch_persona` - Switch between personas
- `get_persona_checklist` - Get persona review checklist

## Available Personas

1. **business_analyst**
   - Focus: Requirements, user stories, acceptance criteria
   - Hides: Technical implementation details
   - Tools: JIRA, Confluence, Lucidchart

2. **software_engineer**
   - Focus: Code quality, TDD, SOLID principles
   - Coverage: 90% unit, 80% integration
   - Tools: VSCode, Git, pytest, mypy

3. **qa_engineer**
   - Focus: Test coverage, quality gates
   - Levels: 7 testing levels (unit through security)
   - Automation: 80% minimum

4. **data_architect**
   - Focus: Data modeling, schema design
   - Standards: 3NF normalization
   - Artifacts: ERD, data dictionary, migrations

5. **security_engineer**
   - Focus: Vulnerabilities, compliance
   - Testing: SAST, DAST, penetration
   - SLA: 4 hours for critical fixes

6. **devops_engineer**
   - Focus: CI/CD, infrastructure, monitoring
   - Strategy: Blue-green deployments
   - Tools: Terraform, Kubernetes, Prometheus

## Example Workflow

```
User: "List the available personas"
Claude: [uses list_personas tool]
        "Available personas: business_analyst, software_engineer, qa_engineer..."

User: "Load the payment_gateway project context"
Claude: [uses load_context tool]
        "Loaded payment_gateway context. This is a PCI-compliant payment gateway..."

User: "Apply the security_engineer persona"
Claude: [uses apply_persona_to_context tool]
        "Now viewing as Security Engineer. Focus areas: Security testing,
        Vulnerability management, Compliance..."

User: "What should I review in this code?"
Claude: [uses get_persona_checklist tool]
        "Security Engineer Review Checklist:
        □ Are there security vulnerabilities?
        □ Is authentication proper?
        □ Is data encrypted?
        □ Are inputs validated?
        □ Are secrets properly managed?"

User: "Now switch to the qa_engineer persona"
Claude: [uses switch_persona tool]
        "Switched from security_engineer to qa_engineer.
        Added Focus Areas: Test planning, Test automation, Quality assurance
        Removed Focus Areas: Security testing, Vulnerability management"
```

## Troubleshooting

### Server Not Showing in Claude Desktop

1. Check the config file exists:
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. Verify MCP SDK is installed:
   ```bash
   python -c "import mcp; print('MCP installed')"
   ```

3. Test server can start:
   ```bash
   cd /Users/jim/src/apps/AI_SDLC_Context
   python mcp_service/server/main.py --help
   ```

4. Check Claude Desktop logs (if available)

### Tools Not Available

1. Ensure Claude Desktop was fully restarted
2. Look for the 🔌 MCP icon in Claude Desktop
3. Ask Claude: "What MCP tools are available?"

## Next Steps

1. **Create Projects**: Use `create_project` to add more configuration projects in `example_projects_repo/`
2. **Add Custom Personas**: Create persona projects as hierarchical configurations
3. **Build Workflows**: Combine contexts via merge tuples for specialized behaviors

## Documentation

- [CONTEXT_MANAGEMENT.md](mcp_service/docs/CONTEXT_MANAGEMENT.md) - Full context management guide
- [PERSONAS.md](mcp_service/docs/PERSONAS.md) - Complete persona system documentation
- [README.md](README.md) - Project overview

---

**Status**: ✅ Configured and ready to use!

To start using:
1. Restart Claude Desktop
2. Start a new conversation
3. Ask: "What MCP tools are available?"
