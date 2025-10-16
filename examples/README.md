# Example Projects - Federated Context Usage

This directory contains **example projects** demonstrating how to use AI_SDLC_Context in various scenarios, including federated multi-server setups.

## Directory Structure

```
examples/
├── local_projects/              # Example local project configurations
│   ├── acme_corporate/         # Corporate-level standards
│   ├── payment_gateway/        # High-risk enterprise project
│   └── admin_dashboard/        # Low-risk internal tool
│
├── federated_setup/            # Example federated configurations
│   └── (to be added)           # Multi-server context composition
│
├── merged_projects/            # Example merged/deployed configs
│   └── payment_gateway_prod_v1_0_0/
│
├── projects.json               # Registry of example projects
└── README.md                   # This file
```

---

## Baseline vs Local Contexts

### Baseline Contexts (`/contexts/`)

These are **read-only reference contexts** provided by AI_SDLC_Context:
- `aisdlc_methodology` - Core Sacred Seven principles and TDD workflow
- `python_standards` - Python language standards and best practices

**Use case**: Install once, reference from multiple projects

### Local Contexts (`/examples/local_projects/`)

These are **customized configurations** for your organization/division/team:
- Corporate policies (e.g., `acme_corporate`)
- Division-specific standards
- Team customizations
- Individual project configs

**Use case**: Customize and extend baseline contexts for your needs

---

## Federated Context Architecture

### Concept

Multiple MCP context servers provide contexts that you can compose:

```
┌────────────────────────────────────────────────────────────┐
│ Your Development Environment                               │
│                                                             │
│ Connected MCP Context Services:                            │
│ ├─ corporate (mcp://contexts.corporate.com:8000)          │
│ ├─ division  (mcp://eng-division.local:8000)              │
│ └─ local     (mcp://localhost:8000)                       │
└────────────────────────────────────────────────────────────┘
```

### Context Tuple Composition

Contexts are loaded as **layers** with priority-based merging:

```yaml
# .aisdlc_context/contexts_list.json (in your project root)
{
  "servers": {
    "corporate": "mcp://contexts.corporate.com:8000",
    "division": "mcp://eng-division.local:8000",
    "local": "mcp://localhost:8000"
  },
  "context_tuple": [
    "corporate.aisdlc_methodology",     # Layer 0: Base methodology
    "corporate.python_standards",       # Layer 1: Language standards
    "division.engineering_standards",   # Layer 2: Division overrides
    "local.backend_team",               # Layer 3: Team customizations
    "local.my_payment_api"              # Layer 4: Project-specific
  ],
  "merge_strategy": "priority",         # Later layers override earlier
  "cache_policy": {
    "corporate": "24h",
    "division": "1h",
    "local": "none"
  }
}
```

**Merge Order**: `corporate` → `division` → `local` (later overrides earlier)

---

## Usage Examples

### Example 1: Single Server (Local Development)

```bash
# Start local MCP context service
cd /path/to/AI_SDLC_Context
python -m mcp_service.server --port 8000

# In your project directory, create context configuration
cat > .aisdlc_context/contexts_list.json <<EOF
{
  "servers": {
    "local": "mcp://localhost:8000"
  },
  "context_tuple": [
    "local.aisdlc_methodology",
    "local.python_standards"
  ]
}
EOF

# Load contexts via MCP (from Claude Code or other client)
# The MCP service will merge the contexts and provide unified config
```

### Example 2: Corporate + Local

```bash
# Connect to corporate context server (read-only)
# and local server (read-write)

cat > .aisdlc_context/contexts_list.json <<EOF
{
  "servers": {
    "corporate": "mcp://contexts.corporate.com:8000",
    "local": "mcp://localhost:8000"
  },
  "context_tuple": [
    "corporate.aisdlc_methodology",    # From corporate
    "corporate.python_standards",      # From corporate
    "local.my_team_customizations",    # Local overrides
    "local.my_api_project"             # This project
  ]
}
EOF
```

### Example 3: Three-Tier (Corporate → Division → Local)

```bash
# Full federated setup
cat > .aisdlc_context/contexts_list.json <<EOF
{
  "servers": {
    "corporate": "mcp://contexts.corporate.com:8000",
    "division": "mcp://eng-division.local:8000",
    "local": "mcp://localhost:8000"
  },
  "context_tuple": [
    "corporate.aisdlc_methodology",
    "corporate.python_standards",
    "corporate.security_baseline",
    "division.python_standards",        # Overrides corporate python
    "division.engineering_process",
    "local.backend_team",
    "local.payment_api"
  ],
  "merge_strategy": "priority"
}
EOF
```

---

## Example Projects Explained

### acme_corporate/

**Purpose**: Demonstrates organizational-level configuration
**Inherits**: `aisdlc_methodology`
**Adds**: Corporate policies, compliance requirements, approval workflows

**Use case**: Your company's context server would host this

### payment_gateway/

**Purpose**: High-risk payment processing service
**Inherits**: `aisdlc_methodology`, `python_standards`, `acme_corporate`
**Adds**: Strict security requirements, high test coverage (95%), PCI compliance

**Use case**: Mission-critical service with elevated standards

### admin_dashboard/

**Purpose**: Low-risk internal admin tool
**Inherits**: `aisdlc_methodology`, `python_standards`, `acme_corporate`
**Adds**: Relaxed requirements for internal tooling

**Use case**: Rapid development for internal tools

---

## Project Initialization Workflow

### Step 1: Set Up Context Servers

```bash
# Corporate server (managed by IT)
# Hosts: aisdlc_methodology, python_standards, security_baseline, etc.

# Division server (managed by engineering team)
# Hosts: division-specific standards and processes

# Local server (you run it)
cd /path/to/AI_SDLC_Context
python -m mcp_service.server --port 8000 --data-dir ~/my_contexts
```

### Step 2: Initialize New Project

```bash
# In your new project directory
mkdir .aisdlc_context

# Create context configuration
cat > .aisdlc_context/contexts_list.json <<EOF
{
  "servers": {
    "corporate": "mcp://contexts.corporate.com:8000",
    "local": "mcp://localhost:8000"
  },
  "context_tuple": [
    "corporate.aisdlc_methodology",
    "corporate.python_standards",
    "local.my_new_project"
  ]
}
EOF

# Create empty project context
cat > .aisdlc_context/config.yml <<EOF
project:
  name: "my_new_project"
  type: "api_service"

# Add project-specific overrides here
EOF
```

### Step 3: Load Context in Development

```bash
# Claude Code with MCP plugin automatically:
# 1. Reads .aisdlc_context/contexts_list.json
# 2. Connects to specified servers
# 3. Loads and merges context tuple
# 4. Provides unified configuration

# You can now query the merged context:
# - What testing standards apply?
# - What's the code review process?
# - What security requirements must I meet?
```

---

## Creating Your Own Contexts

### 1. Start with Examples

Copy an example project and customize:

```bash
cp -r examples/local_projects/payment_gateway my_contexts/my_service
cd my_contexts/my_service

# Edit project.json
# Edit config/config.yml
# Customize for your needs
```

### 2. Register with Local Server

```bash
# Add to your local context server's registry
cat >> ~/my_contexts/contexts.json <<EOF
{
  "my_service": {
    "type": "project",
    "path": "my_service",
    "base_contexts": ["aisdlc_methodology", "python_standards"],
    "description": "My custom service configuration"
  }
}
EOF
```

### 3. Reference in Context Tuple

```json
{
  "context_tuple": [
    "corporate.aisdlc_methodology",
    "local.my_service"
  ]
}
```

---

## Best Practices

### 1. Layer Your Contexts

- **Layer 0**: Methodology (aisdlc_methodology)
- **Layer 1**: Language standards (python_standards)
- **Layer 2**: Organizational policies (acme_corporate)
- **Layer 3**: Division/team customizations
- **Layer 4**: Project-specific config

### 2. Use Appropriate Servers

- **Corporate server**: Baseline standards, read-only
- **Division server**: Team-specific, managed by team leads
- **Local server**: Your personal/project configs, full control

### 3. Override Strategically

Don't override everything - only customize what's needed:

```yaml
# Good: Specific override
testing:
  coverage_minimum: 95  # Higher than baseline 80%

# Bad: Copying entire config
# (defeats purpose of inheritance)
```

### 4. Document Overrides

```yaml
# Always explain why you're overriding
testing:
  coverage_minimum: 95  # Payment processing requires higher coverage
```

---

## Troubleshooting

### Context Not Found

```
Error: Context 'corporate.aisdlc_methodology' not found
```

**Solution**: Check server connectivity and context exists:
```bash
mcp list-contexts --server corporate
```

### Merge Conflicts

```
Warning: Conflicting values at path 'testing.coverage_minimum'
```

**Solution**: Check merge strategy and layer order

### Cache Issues

```
Error: Stale context from division server
```

**Solution**: Clear cache or adjust cache policy

---

## Next Steps

1. **Run local examples**: See `/examples/local_projects/`
2. **Set up your context server**: See MCP service docs
3. **Create your first context tuple**: Start with corporate + local
4. **Customize for your team**: Add division/team layer
5. **Deploy to projects**: Use `.aisdlc_context/` in each project

For more information:
- [MCP Service Documentation](../mcp_service/docs/)
- [Baseline Contexts](../contexts/)
- [Context Tutorial](./tutorial/)
