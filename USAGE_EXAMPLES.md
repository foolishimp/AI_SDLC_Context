# Usage Examples - AI_SDLC_config

Practical examples showing different ways to use the system.

## Table of Contents
- [Run Built-in Demos](#run-built-in-demos)
- [Python API Examples](#python-api-examples)
- [Claude Desktop Examples](#claude-desktop-examples)
- [Real-World Scenarios](#real-world-scenarios)

---

## Run Built-in Demos

The fastest way to see the system in action:

```bash
cd /Users/jim/src/apps/AI_SDLC_config

# Demo 1: Project Management
python mcp_service/examples/direct_usage_example.py
```

**What you'll see:**
- Creating corporate base configuration
- Adding Python methodology
- Creating payment_gateway project
- Merging configurations with priority
- Git audit trail

```bash
# Demo 2: Context Management  
python mcp_service/examples/context_management_demo.py
```

**What you'll see:**
- Loading payment_gateway context
- Claude sees PCI compliance requirements
- Switching to admin_dashboard context
- Claude adapts to simpler requirements
- Requirement change detection

```bash
# Demo 3: Persona System
python mcp_service/examples/persona_demo.py
```

**What you'll see:**
- 6 personas viewing same project
- Business Analyst: focuses on requirements
- Security Engineer: focuses on vulnerabilities
- QA Engineer: focuses on test coverage
- Each persona has different checklist

---

## Python API Examples

### Example 1: Create a New Project

```python
from pathlib import Path
from mcp_service.storage.project_repository import ProjectRepository

# Initialize
repo = ProjectRepository(Path("projects_repo"))

# Create project
metadata = repo.create_project(
    name="my_api",
    project_type="custom",
    base_projects=["corporate_base", "python_methodology"],
    config={
        "project": {
            "name": "my_api",
            "description": "RESTful API service"
        },
        "testing": {
            "min_coverage": 90
        }
    },
    description="My REST API"
)

print(f"Created: {metadata.name}")
print(f"Git commit: {metadata.last_git_commit}")
```

### Example 2: Load Context

```python
from pathlib import Path
from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager

repo = ProjectRepository(Path("projects_repo"))
context_mgr = ContextManager(repo)

# Load context
context = context_mgr.load_context("payment_gateway")

# Access merged configuration
print(f"PCI Compliant: {context['project']['pci_compliant']}")
print(f"Min Coverage: {context['requirements']['testing']['min_coverage']}%")
print(f"Encryption: {context['requirements']['security']['encryption']}")
```

### Example 3: Apply Persona

```python
from pathlib import Path
from mcp_service.storage.project_repository import ProjectRepository
from mcp_service.server.context_tools import ContextManager
from mcp_service.server.persona_manager import PersonaManager

repo = ProjectRepository(Path("projects_repo"))
context_mgr = ContextManager(repo)
persona_mgr = PersonaManager(Path("personas"))

# Load project + persona
base_context = context_mgr.load_context("payment_gateway")
persona = persona_mgr.load_persona("security_engineer")
security_view = persona_mgr.apply_persona_to_context(base_context, persona)

# See security-specific requirements
print("Security Engineer Focus:")
for focus in security_view['active_persona']['focus_areas']:
    print(f"  • {focus}")

# Get security checklist
checklist = persona_mgr.get_persona_review_checklist("security_engineer")
print("\nReview Checklist:")
for item in checklist:
    print(f"  □ {item}")
```

---

## Claude Desktop Examples

### Setup First

```bash
# Install MCP SDK
pip install mcp

# Configuration already created at:
# ~/Library/Application Support/Claude/claude_desktop_config.json

# Restart Claude Desktop
```

### Example 1: Explore the System

**Conversation:**

```
You: "What MCP tools are available from ai-sdlc-config?"

Claude: I can see 20 MCP tools available:
        
        Project Management (11 tools):
        • create_project, get_project, list_projects
        • update_project, delete_project
        • add_node, remove_node, add_document
        • merge_projects, inspect_project, compare_projects
        
        Context Management (4 tools):
        • load_context, switch_context
        • query_context, get_current_context
        
        Persona Management (5 tools):
        • list_personas, load_persona
        • apply_persona_to_context, switch_persona
        • get_persona_checklist
```

### Example 2: Load Context for Code Generation

```
You: "List the available projects"

Claude: [uses list_projects]
        Available projects:
        • payment_gateway - PCI-compliant payment processing
        • admin_dashboard - Internal admin interface

You: "Load the payment_gateway context"

Claude: [uses load_context]
        Loaded payment_gateway context:
        - Classification: restricted
        - PCI Compliant: Yes
        - Min Coverage: 95%
        - Encryption: AES-256
        - Fraud Detection: Enabled
        
        I'm now aware of these requirements.

You: "Write a function to process a payment"

Claude: Based on the payment_gateway context, I'll write PCI-compliant code
        with encryption and fraud detection:
        
        [Generates code with:]
        - Input validation
        - AES-256 encryption
        - Fraud detection hooks
        - Audit logging
        - Error handling
        - Comprehensive tests (95% coverage)
```

### Example 3: Use Personas for Code Review

```
You: "List available personas"

Claude: [uses list_personas]
        6 personas available:
        • business_analyst - Requirements focus
        • software_engineer - Code quality focus
        • qa_engineer - Testing focus
        • data_architect - Data modeling focus
        • security_engineer - Security focus
        • devops_engineer - Deployment focus

You: "Apply security_engineer persona and review this code: [paste code]"

Claude: [uses apply_persona_to_context]
        [uses get_persona_checklist]
        
        Reviewing as Security Engineer:
        
        Security Review Checklist:
        □ Are there security vulnerabilities?
          ⚠️  SQL injection possible on line 45
        
        □ Is authentication proper?
          ✅ JWT validation looks good
        
        □ Is data encrypted?
          ❌ Passwords stored in plaintext
        
        □ Are inputs validated?
          ⚠️  Missing validation on user input
        
        □ Are secrets properly managed?
          ❌ API key hardcoded in source

You: "Now review as qa_engineer"

Claude: [uses switch_persona]
        Switched to QA Engineer persona.
        
        Testing Review Checklist:
        □ Are there adequate tests?
          ⚠️  Only 60% coverage (need 80%+)
        
        □ Are edge cases covered?
          ❌ Missing null checks
        
        □ Is test automation present?
          ✅ Good pytest integration
```

### Example 4: Context Switching

```
You: "Load payment_gateway context and generate a payment handler"

Claude: [uses load_context]
        [Generates strict, PCI-compliant code with heavy security]

You: "Now switch to admin_dashboard context and generate a user list view"

Claude: [uses switch_context]
        Switched contexts. Requirements changed:
        • Classification: restricted → internal
        • Coverage: 95% → 85%
        • Security: PCI compliance → basic auth
        
        [Generates simpler, internal-use code]
```

---

## Real-World Scenarios

### Scenario 1: Multi-Project Development

**Setup:**
```bash
# Run demo to create sample projects
python mcp_service/examples/direct_usage_example.py
```

**In Claude Desktop:**
```
You: "I'm working on three projects today. Show me what's available."

Claude: [uses list_projects]
        • payment_gateway - Restricted, PCI-compliant
        • admin_dashboard - Internal tools
        • mobile_app - Customer-facing app

You: "Load payment_gateway and help me implement fraud detection"

Claude: [Generates code appropriate for payment_gateway context]

You: "Now switch to mobile_app and help with the login screen"

Claude: [Switches context, generates mobile-appropriate code]
```

### Scenario 2: Team Code Review

**Setup:** Each team member uses appropriate persona.

**QA Engineer:**
```
You: "Apply qa_engineer persona and review for test coverage"

Claude: [Focuses on:]
        • Test coverage metrics
        • Edge cases
        • Automation
        • Quality gates
```

**Security Engineer:**
```
You: "Apply security_engineer persona and review for vulnerabilities"

Claude: [Focuses on:]
        • SAST findings
        • Authentication issues
        • Encryption
        • Input validation
```

**DevOps Engineer:**
```
You: "Apply devops_engineer persona and review for deployability"

Claude: [Focuses on:]
        • Deployment scripts
        • Rollback capability
        • Monitoring hooks
        • Infrastructure code
```

### Scenario 3: Compliance Audit

**Setup:** Create restricted project with compliance requirements.

**In Claude Desktop:**
```
You: "Load payment_gateway context and apply security_engineer persona"

Claude: [Combined view showing:]
        • PCI compliance requirements
        • Security testing requirements
        • 4-hour critical fix SLA
        • Continuous scanning

You: "Audit this codebase against PCI requirements"

Claude: [Generates comprehensive audit report:]
        • ✅ Encryption: AES-256
        • ✅ Access controls: Proper
        • ⚠️  Logging: Incomplete
        • ❌ Key rotation: Not implemented
```

---

## Tips and Tricks

### Tip 1: Combine Context + Persona

```
"Load payment_gateway context and apply security_engineer persona"
→ Most restrictive view: PCI compliance + security focus
```

### Tip 2: Switch Personas Mid-Review

```
"Apply qa_engineer persona"
[Review from testing perspective]

"Switch to devops_engineer persona"  
[Same code, deployment perspective]
```

### Tip 3: Query Current Context

```
"What context am I currently in?"
"What are the testing requirements?"
"What security standards apply?"
```

### Tip 4: Create Custom Personas

```bash
# Copy existing persona
cp personas/security_engineer.yml personas/custom_role.yml

# Edit to customize focus areas, tools, overrides
nano personas/custom_role.yml
```

---

## Next Steps

1. **Run all demos** to see the system in action
2. **Set up Claude Desktop** for MCP integration
3. **Try the examples** in your own conversations
4. **Create custom projects** for your team
5. **Add custom personas** for your roles

## More Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [MCP_SETUP.md](MCP_SETUP.md) - Claude Desktop setup
- [CONTEXT_MANAGEMENT.md](mcp_service/docs/CONTEXT_MANAGEMENT.md) - Context system
- [PERSONAS.md](mcp_service/docs/PERSONAS.md) - Persona system

---

**Start using AI_SDLC_config now!** 🚀
