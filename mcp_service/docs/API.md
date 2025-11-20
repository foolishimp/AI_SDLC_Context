# MCP Service API Reference

Complete reference for all MCP tools provided by the ai_sdlc_method service.

## Table of Contents

1. [Project Management](#project-management)
   - [create_project](#create_project)
   - [get_project](#get_project)
   - [list_projects](#list_projects)
   - [update_project](#update_project)
   - [delete_project](#delete_project)

2. [Content Management](#content-management)
   - [add_node](#add_node)
   - [remove_node](#remove_node)
   - [add_document](#add_document)

3. [Merge Operations](#merge-operations)
   - [merge_projects](#merge_projects)

4. [LLM Inspection](#llm-inspection)
   - [inspect_project](#inspect_project)
   - [compare_projects](#compare_projects)

---

## Project Management

### create_project

Create a new configuration project in the repository.

**Input Schema:**

```json
{
  "name": "string (required)",
  "type": "string (required, enum: base|methodology|custom)",
  "base_projects": ["array of strings (required)"],
  "config": "object (optional)",
  "description": "string (optional)"
}
```

**Example:**

```json
{
  "name": "payment_service",
  "type": "custom",
  "base_projects": ["corporate_base", "python_methodology"],
  "config": {
    "project": {
      "name": "Payment Service",
      "team": "Payments Team"
    },
    "methodology": {
      "testing": {
        "min_coverage": 95
      }
    }
  },
  "description": "Payment processing microservice"
}
```

**Response:**

```json
{
  "name": "payment_service",
  "project_type": "custom",
  "version": "1.0.0",
  "created": "2024-10-15T10:30:00Z",
  "modified": "2024-10-15T10:30:00Z",
  "base_projects": ["corporate_base", "python_methodology"],
  "description": "Payment processing microservice",
  "merged_from": null,
  "merge_date": null,
  "runtime_overrides": null
}
```

**Storage:**

```
projects_repo/
└── payment_service/
    ├── project.json        # Metadata
    ├── config/
    │   └── config.yml      # Configuration
    └── docs/               # Documentation directory
```

---

### get_project

Retrieve metadata for a specific project.

**Input Schema:**

```json
{
  "name": "string (required)"
}
```

**Example:**

```json
{
  "name": "payment_service"
}
```

**Response:**

Returns the same structure as `create_project` response, or:

```
Project 'payment_service' not found
```

---

### list_projects

List all projects in the repository.

**Input Schema:**

```json
{}
```

**Example:**

```json
{}
```

**Response:**

```json
[
  {
    "name": "corporate_base",
    "type": "base",
    "base_projects": [],
    "description": "Corporate policies and standards"
  },
  {
    "name": "python_methodology",
    "type": "methodology",
    "base_projects": ["corporate_base"],
    "description": "Python-specific standards"
  },
  {
    "name": "payment_service",
    "type": "custom",
    "base_projects": ["corporate_base", "python_methodology"],
    "description": "Payment processing microservice"
  }
]
```

---

### update_project

Update project configuration values.

**Input Schema:**

```json
{
  "name": "string (required)",
  "updates": "object (required)"
}
```

The `updates` object uses **dot notation** for paths:

```json
{
  "name": "payment_service",
  "updates": {
    "methodology.testing.min_coverage": 98,
    "security.vulnerability_management.critical_fix_sla_hours": 2,
    "quality.gates.max_critical_issues": 0
  }
}
```

**Response:**

Returns updated `ProjectMetadata`.

---

### delete_project

Delete a project from the repository.

**Input Schema:**

```json
{
  "name": "string (required)"
}
```

**Example:**

```json
{
  "name": "old_project"
}
```

**Response:**

```
Project 'old_project' deleted successfully
```

---

## Content Management

### add_node

Add a configuration node to a project.

**Input Schema:**

```json
{
  "project": "string (required)",
  "path": "string (required, dot-delimited)",
  "value": "any (required)"
}
```

**Example:**

```json
{
  "project": "payment_service",
  "path": "security.fraud_detection",
  "value": {
    "enabled": true,
    "threshold": 85,
    "real_time": true
  }
}
```

**Result:**

Adds/updates the node at the specified path in the project configuration.

**Response:**

```
Added node 'security.fraud_detection' to project 'payment_service'
```

---

### remove_node

Remove a configuration node from a project.

**Input Schema:**

```json
{
  "project": "string (required)",
  "path": "string (required, dot-delimited)"
}
```

**Example:**

```json
{
  "project": "payment_service",
  "path": "old_config.deprecated"
}
```

**Response:**

```
Removed node 'old_config.deprecated' from project 'payment_service'
```

---

### add_document

Add a documentation file to a project.

**Input Schema:**

```json
{
  "project": "string (required)",
  "path": "string (required, relative path within docs/)",
  "content": "string (required)"
}
```

**Example:**

```json
{
  "project": "payment_service",
  "path": "policies/pci_compliance.md",
  "content": "# PCI Compliance\n\n## Requirements\n- SAQ D certification\n- Annual audits\n..."
}
```

**Storage:**

```
projects_repo/
└── payment_service/
    └── docs/
        └── policies/
            └── pci_compliance.md
```

**Response:**

```
Document added at: /path/to/projects_repo/payment_service/docs/policies/pci_compliance.md
```

**Referencing in Config:**

```yaml
# In payment_service/config/config.yml
projects:
  payment_service:
    docs:
      pci_compliance:
        uri: "file://docs/policies/pci_compliance.md"
```

---

## Merge Operations

### merge_projects

Merge multiple projects into a new merged project.

**Input Schema:**

```json
{
  "source_projects": ["array of strings (required)"],
  "target_project": "string (required)",
  "runtime_overrides": "object (optional)",
  "description": "string (optional)"
}
```

**Example:**

```json
{
  "source_projects": [
    "corporate_base",
    "python_methodology",
    "payment_service"
  ],
  "target_project": "payment_service_production",
  "runtime_overrides": {
    "environment": "production",
    "security.vulnerability_management.scan_frequency": "continuous"
  },
  "description": "Production deployment configuration"
}
```

**Merge Priority:**

Projects are merged in order (left to right), with later projects overriding earlier ones:

```
corporate_base (priority 0)
  ↓
python_methodology (priority 1) - overrides corporate_base
  ↓
payment_service (priority 2) - overrides python_methodology
  ↓
runtime_overrides (priority 3) - highest priority
```

**Response:**

```json
{
  "name": "payment_service_production",
  "project_type": "merged",
  "version": "1.0.0",
  "created": "2024-10-15T14:30:00Z",
  "modified": "2024-10-15T14:30:00Z",
  "base_projects": ["corporate_base", "python_methodology", "payment_service"],
  "description": "Production deployment configuration",
  "merged_from": ["corporate_base", "python_methodology", "payment_service"],
  "merge_date": "2024-10-15T14:30:00Z",
  "runtime_overrides": {
    "environment": "production",
    "security.vulnerability_management.scan_frequency": "continuous"
  }
}
```

**Storage:**

```
projects_repo/
└── merged_projects/
    └── payment_service_production/
        ├── project.json        # Metadata with merge info
        ├── config/
        │   └── merged.yml      # Full merged configuration
        └── .merge_info.json    # Merge provenance
```

**Key Distinction:**

| Aspect | Custom Project | Merged Project |
|--------|---------------|----------------|
| **Type** | `custom` | `merged` |
| **Creation** | Manual YAML | Auto-generated merge |
| **Config File** | `config.yml` (overrides only) | `merged.yml` (full config) |
| **Mutability** | Living config | Immutable snapshot |
| **Metadata** | `base_projects` | `merged_from`, `merge_date`, `runtime_overrides` |
| **Use Case** | Development | Deployment |

---

## LLM Inspection

### inspect_project

Query and inspect a project using natural language (LLM-powered).

**Input Schema:**

```json
{
  "project": "string (required)",
  "query": "string (required)"
}
```

**Example:**

```json
{
  "project": "payment_service",
  "query": "What are the security requirements and testing standards?"
}
```

**Response:**

Returns the project configuration formatted for LLM analysis with the query context:

```
Project: payment_service

Query: What are the security requirements and testing standards?

Configuration:
corporate:
  policies:
    security:
      uri: file://docs/policies/security.md
      content: "# Security Policy..."
methodology:
  testing:
    min_coverage: 95
    required_types:
      - unit
      - integration
      - security
security:
  vulnerability_management:
    critical_fix_sla_hours: 4
    scan_frequency: daily
...
```

This is designed to be processed by an LLM (Claude, GPT, etc.) to answer the natural language query.

---

### compare_projects

Compare two projects and highlight differences (LLM-powered).

**Input Schema:**

```json
{
  "project1": "string (required)",
  "project2": "string (required)",
  "query": "string (optional)"
}
```

**Example:**

```json
{
  "project1": "payment_service",
  "project2": "internal_dashboard",
  "query": "Compare testing requirements and security standards"
}
```

**Response:**

Returns both project configurations formatted for comparison:

```
Comparison: payment_service vs internal_dashboard

Focus: Compare testing requirements and security standards

payment_service Configuration:
methodology:
  testing:
    min_coverage: 95
security:
  vulnerability_management:
    critical_fix_sla_hours: 4
...

internal_dashboard Configuration:
methodology:
  testing:
    min_coverage: 75
security:
  vulnerability_management:
    critical_fix_sla_hours: 24
...
```

---

## Error Handling

All tools return errors in the following format:

```
Error: Project 'nonexistent' not found
```

```
Error: Source project 'missing_project' not found
```

```
Error: Target project 'already_exists' already exists
```

---

## Git Integration

All operations that modify the repository are automatically committed:

```bash
# Project creation
git commit -m "Create project: payment_service"

# Project update
git commit -m "Update project: payment_service"

# Document addition
git commit -m "Add document to payment_service: docs/architecture.md"

# Merge operation
git commit -m "Merge projects into payment_service_production: corporate_base, python_methodology, payment_service"

# Project deletion
git commit -m "Delete project: old_project"
```

View history:

```bash
cd projects_repo
git log --oneline
```

---

## Best Practices

### 1. Project Naming

- Use `snake_case` for project names
- Use descriptive names: `payment_service`, not `ps`
- Prefix methodology projects: `python_methodology`, `javascript_methodology`

### 2. Project Types

- **Base**: Corporate foundations, shared policies
- **Methodology**: Language/framework standards
- **Custom**: Project-specific configurations
- **Merged**: Auto-generated deployment snapshots (don't create manually)

### 3. Configuration Structure

Use hierarchical structure with dot notation:

```yaml
corporate:
  policies:
    security: {...}
    code_review: {...}

methodology:
  testing: {...}
  coding: {...}
  deployment: {...}

project:
  name: "..."
  team: "..."

security:
  vulnerability_management: {...}

quality:
  gates: {...}
```

### 4. Merge Strategy

Order source projects by priority (low to high):

```json
{
  "source_projects": [
    "corporate_base",        // Lowest priority
    "python_methodology",    // Overrides corporate
    "payment_service"        // Highest priority (most specific)
  ]
}
```

### 5. Runtime Overrides

Use for environment-specific or deployment-time settings:

```json
{
  "runtime_overrides": {
    "environment": "production",
    "deployment.timestamp": "2024-10-15T14:30:00Z",
    "build.version": "1.2.3"
  }
}
```

---

## Integration Examples

### CI/CD Pipeline

```python
from mcp import ClientSession

async def deploy_to_production(project_name):
    async with get_mcp_session() as session:
        # Merge project for production
        result = await session.call_tool(
            "merge_projects",
            arguments={
                "source_projects": [
                    "corporate_base",
                    "python_methodology",
                    project_name
                ],
                "target_project": f"{project_name}_prod_{timestamp}",
                "runtime_overrides": {
                    "environment": "production",
                    "build.version": get_version(),
                    "deployment.timestamp": datetime.now().isoformat()
                }
            }
        )

        # Get merged config for validation
        config = get_project_config(f"{project_name}_prod_{timestamp}")

        # Validate quality gates
        min_coverage = config.get_value("methodology.testing.min_coverage")
        if actual_coverage < min_coverage:
            raise Exception(f"Coverage below minimum: {actual_coverage}% < {min_coverage}%")

        # Deploy...
```

### Documentation Portal

```python
async def get_project_docs(project_name):
    async with get_mcp_session() as session:
        # Inspect project
        result = await session.call_tool(
            "inspect_project",
            arguments={
                "project": project_name,
                "query": "List all documentation and policies"
            }
        )

        # LLM processes the configuration and returns structured docs list
        return parse_llm_response(result)
```

---

## See Also

- [MCP Service README](../README.md) - Overview and architecture
- [Direct Usage Example](../examples/direct_usage_example.py) - Python API usage
- [MCP Client Example](../examples/mcp_client_example.py) - MCP protocol usage
- [Corporate SDLC Example](../../examples/corporate_sdlc/) - Real-world use case
