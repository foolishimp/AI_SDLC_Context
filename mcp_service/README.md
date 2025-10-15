# AI_SDLC_Context MCP Service

Model Context Protocol (MCP) service for managing AI_SDLC configuration projects.

## Overview

This MCP service provides:
1. **Project CRUD** - Create, Read, Update, Delete configuration projects
2. **Content CRUD** - Manage nodes, documents, and configuration values
3. **LLM Inspection** - Query and inspect projects using natural language
4. **Merge Operations** - Merge multiple projects to create new configurations
5. **Repository Storage** - Projects stored in git-friendly structure

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ MCP Client (Claude, CLI, etc.)                     │
└────────────────┬────────────────────────────────────┘
                 │ MCP Protocol
┌────────────────▼────────────────────────────────────┐
│ MCP Server                                          │
│  ├─ Project Management (CRUD)                      │
│  ├─ Content Management (nodes, docs)               │
│  ├─ Merge Engine (multi-project merge)             │
│  └─ Inspection Tools (LLM queries)                 │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│ Project Repository                                  │
│  projects/                                          │
│    ├─ corporate_base/                              │
│    ├─ python_methodology/                          │
│    ├─ payment_service/                             │
│    ├─ internal_dashboard/                          │
│    └─ merged_projects/                             │
│        └─ payment_service_production/              │
└─────────────────────────────────────────────────────┘
```

## Key Concepts

### 1. Projects
A **project** is a self-contained configuration unit with:
- Metadata (name, version, type, base projects)
- Configuration YAML files
- Documentation files (referenced by URIs)
- Git history

### 2. Project Types
- **Base Project**: Foundation projects (e.g., `corporate_base`)
- **Methodology Project**: Language/framework specific (e.g., `python_methodology`)
- **Custom Project**: Project-specific overrides (e.g., `payment_service`)
- **Merged Project**: Result of merging multiple projects (e.g., `payment_service_prod`)

### 3. Merge vs Custom Override

**Custom Override Project**:
```yaml
# projects/payment_service/config.yml
# Manually created, inherits from base
project:
  name: "Payment Service"

methodology:
  testing:
    min_coverage: 95  # Manual override
```

**Merged Project**:
```yaml
# Automatically generated from merge operation
# Source: corporate_base + python_methodology + payment_service + runtime
project:
  name: "Payment Service Production"
  merged_from:
    - "corporate_base"
    - "python_methodology"
    - "payment_service"
  merge_date: "2024-10-15T10:30:00Z"

# Contains full merged configuration
methodology:
  testing:
    min_coverage: 95  # Result of merge
```

## MCP Service Operations

### Project CRUD

#### Create Project
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_project",
    "arguments": {
      "name": "new_microservice",
      "type": "custom",
      "base_projects": ["corporate_base", "python_methodology"],
      "config": {...}
    }
  }
}
```

#### Read Project
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_project",
    "arguments": {
      "name": "payment_service"
    }
  }
}
```

#### Update Project
```json
{
  "method": "tools/call",
  "params": {
    "name": "update_project",
    "arguments": {
      "name": "payment_service",
      "updates": {
        "methodology.testing.min_coverage": 98
      }
    }
  }
}
```

#### Delete Project
```json
{
  "method": "tools/call",
  "params": {
    "name": "delete_project",
    "arguments": {
      "name": "old_project"
    }
  }
}
```

### Content CRUD

#### Add Node
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_node",
    "arguments": {
      "project": "payment_service",
      "path": "security.fraud_detection",
      "value": {"enabled": true, "threshold": 85}
    }
  }
}
```

#### Remove Node
```json
{
  "method": "tools/call",
  "params": {
    "name": "remove_node",
    "arguments": {
      "project": "payment_service",
      "path": "old_config.deprecated"
    }
  }
}
```

#### Add Document
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_document",
    "arguments": {
      "project": "payment_service",
      "path": "docs/new_policy.md",
      "content": "# New Policy..."
    }
  }
}
```

### Merge Operations

#### Merge Projects
```json
{
  "method": "tools/call",
  "params": {
    "name": "merge_projects",
    "arguments": {
      "source_projects": [
        "corporate_base",
        "python_methodology",
        "payment_service"
      ],
      "target_project": "payment_service_production",
      "runtime_overrides": {
        "environment": "production"
      }
    }
  }
}
```

### LLM Inspection

#### Inspect Project
```json
{
  "method": "tools/call",
  "params": {
    "name": "inspect_project",
    "arguments": {
      "project": "payment_service",
      "query": "What are the security requirements?"
    }
  }
}
```

#### Compare Projects
```json
{
  "method": "tools/call",
  "params": {
    "name": "compare_projects",
    "arguments": {
      "project1": "payment_service",
      "project2": "internal_dashboard",
      "query": "What are the differences in testing requirements?"
    }
  }
}
```

## Installation

```bash
cd mcp_service
pip install -e .
```

## Running the Service

```bash
# Start MCP server
python -m mcp_service.server.main --port 8080

# Or as MCP stdio server (for Claude Desktop)
python -m mcp_service.server.main --stdio
```

## Usage with Claude Desktop

Add to Claude Desktop configuration:
```json
{
  "mcpServers": {
    "ai-sdlc-config": {
      "command": "python",
      "args": ["-m", "mcp_service.server.main", "--stdio"],
      "cwd": "/path/to/AI_SDLC_Context/mcp_service"
    }
  }
}
```

## Project Repository Structure

```
projects_repo/
├── .git/                           # Git repository
├── projects.json                   # Project registry
├── corporate_base/
│   ├── project.json               # Project metadata
│   ├── config/
│   │   └── base.yml              # Configuration
│   └── docs/
│       └── policies/
│           └── security.md       # Referenced documents
├── python_methodology/
│   ├── project.json
│   ├── config/
│   │   └── standards.yml
│   └── docs/
│       └── coding_standards.md
├── payment_service/
│   ├── project.json
│   ├── config/
│   │   └── overrides.yml
│   └── docs/
│       └── architecture.md
└── merged_projects/
    └── payment_service_prod/
        ├── project.json           # Contains merge metadata
        ├── config/
        │   └── merged.yml        # Full merged config
        └── .merge_info.json      # Merge provenance
```

## Example Workflows

### 1. Create a New Custom Project

```python
# Via MCP client (Claude)
"Create a new project called 'user_service' based on corporate_base and python_methodology"

# Result: projects/user_service/ created with:
# - project.json (metadata)
# - config/custom.yml (empty override structure)
# - docs/ (documentation directory)
```

### 2. Add Security Policy to Project

```python
# Via MCP client
"Add a new security policy document to payment_service at docs/policies/pci_compliance.md"

# Result: File created and node added to config:
# corporate.policies.pci_compliance:
#   uri: "file://docs/policies/pci_compliance.md"
```

### 3. Merge for Production Deployment

```python
# Via MCP client
"Merge corporate_base, python_methodology, and payment_service into payment_service_production with production environment"

# Result: New merged project created:
# - Full merged configuration
# - Merge metadata (sources, date, overrides)
# - Ready for deployment
```

### 4. Inspect Configuration

```python
# Via MCP client
"What are the testing requirements for payment_service?"

# LLM inspects project and responds:
# "Payment Service requires:
#  - Minimum 95% test coverage
#  - Unit, integration, security, penetration, and load tests
#  - Critical fix SLA: 4 hours
#  - PCI compliance testing"
```

### 5. Compare Projects

```python
# Via MCP client
"Compare testing requirements between payment_service and internal_dashboard"

# LLM compares and responds with differences
```

## Benefits

### For Developers
- ✅ Natural language interface via Claude
- ✅ Git-backed project storage
- ✅ Easy CRUD operations
- ✅ Query configurations without writing code

### For Governance
- ✅ Audit trail (git history)
- ✅ Clear project lineage (merge metadata)
- ✅ Centralized project repository
- ✅ Version control for all changes

### For Operations
- ✅ Generate deployment-ready configs
- ✅ Merge base + methodology + project + runtime
- ✅ Reproducible builds
- ✅ Environment-specific configurations

## API Reference

See `docs/API.md` for complete API documentation.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Start server in dev mode
python -m mcp_service.server.main --debug
```

## License

TBD
