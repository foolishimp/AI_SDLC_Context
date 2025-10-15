# Example Projects Repository

This directory contains example configuration projects for demonstrating the AI_SDLC_Context MCP service and library features.

## Purpose

These example projects showcase:
- **Multi-layer configuration** - Corporate standards, methodology configs, project-specific overrides
- **Project merging** - Combining multiple configuration layers into deployment-ready configs
- **MCP service operations** - CRUD operations, merging, and LLM-based querying
- **Real-world scenarios** - Different risk levels, languages, and organizational standards

## Project Structure

```
example_projects_repo/
├── acme_corporate/          # Corporate-level configuration
│   ├── config/
│   │   └── config.yml       # Corporate policies and standards
│   └── project.json         # Project metadata
│
├── python_standards/        # Language-specific methodology config
│   ├── config/
│   │   └── config.yml       # Python coding standards
│   └── project.json         # Project metadata
│
├── payment_gateway/         # High-risk project example
│   ├── config/
│   │   └── config.yml       # Project-specific overrides
│   ├── docs/
│   │   └── architecture/    # Project documentation
│   └── project.json         # Project metadata
│
├── admin_dashboard/         # Low-risk project example
│   ├── config/
│   │   └── config.yml       # Minimal overrides for internal tool
│   └── project.json         # Project metadata
│
├── merged_projects/         # Auto-generated merged configurations
│   └── payment_gateway_prod_v1_0_0/
│       ├── config/
│       │   └── merged.yml   # Full merged configuration
│       ├── .merge_info.json # Merge metadata
│       └── project.json     # Generated project metadata
│
└── projects.json            # Global project registry
```

## Projects

### 1. acme_corporate
**Type**: Corporate-level configuration
**Purpose**: Defines organization-wide policies

**Features**:
- Security requirements (MFA, encryption, audit logging)
- Code review policies (2 reviewers for high-risk, 1 for low-risk)
- Deployment controls (approval required for production)

### 2. python_standards
**Type**: Methodology configuration
**Purpose**: Python-specific coding standards

**Features**:
- Testing requirements (pytest, coverage thresholds)
- Code quality tools (black, flake8, mypy)
- Documentation standards (docstrings, type hints)

### 3. payment_gateway
**Type**: Project configuration (High-risk)
**Purpose**: Payment processing system

**Features**:
- Risk level: HIGH
- PCI-DSS compliance required
- Strict security and review requirements
- Inherits from: acme_corporate, python_standards

### 4. admin_dashboard
**Type**: Project configuration (Low-risk)
**Purpose**: Internal administrative tool

**Features**:
- Risk level: LOW
- Relaxed requirements for internal tools
- Single reviewer sufficient
- Inherits from: acme_corporate, python_standards

### 5. merged_projects/
**Type**: Generated configurations
**Purpose**: Deployment-ready merged configurations

**Contains**:
- Full merged YAML with all layers combined
- Merge metadata (sources, date, overrides)
- Immutable snapshots for versioned deployments

## Usage with MCP Service

### 1. Query Projects
```python
# List all projects
mcp.call_tool("list_projects", {})

# Get specific project
mcp.call_tool("get_project", {"project_id": "payment_gateway"})
```

### 2. Merge Configurations
```python
# Merge multiple layers for deployment
mcp.call_tool("merge_projects", {
    "project_ids": ["acme_corporate", "python_standards", "payment_gateway"],
    "output_project_id": "payment_gateway_prod_v1_0_0"
})
```

### 3. Query with LLM
```python
# Ask questions about configuration
mcp.call_tool("llm_query_project", {
    "project_id": "payment_gateway",
    "query": "What are the security requirements for this project?"
})
```

## Configuration Hierarchy

The projects demonstrate a 4-layer hierarchy:

```
Layer 1: Corporate Standards (acme_corporate)
    ↓
Layer 2: Methodology Config (python_standards)
    ↓
Layer 3: Project Config (payment_gateway / admin_dashboard)
    ↓
Layer 4: Runtime Overrides (via API/CLI)
```

**Merge Priority**: Layer 4 > Layer 3 > Layer 2 > Layer 1

## Use Cases

### Scenario 1: New Project Setup
1. Start with corporate standards (acme_corporate)
2. Add language methodology (python_standards)
3. Create project-specific config with overrides
4. Merge for deployment

### Scenario 2: Multi-Environment Deployment
1. Base: Corporate + Methodology + Project
2. Dev: Merge with dev overrides (debug enabled)
3. Prod: Merge with prod overrides (strict security)

### Scenario 3: Compliance Auditing
1. Query merged config for security settings
2. Verify inheritance from corporate policies
3. Check project-specific overrides
4. Generate compliance report

## Key Concepts Demonstrated

### 1. Configuration Inheritance
Projects inherit from base configurations and selectively override:
```yaml
# In payment_gateway/config.yml
sdlc:
  security:
    requirements:
      pci_dss_compliance: true  # Override for payment processing
```

### 2. Risk-Based Configuration
Different requirements based on project risk:
- **High-risk** (payment_gateway): 2 reviewers, strict security
- **Low-risk** (admin_dashboard): 1 reviewer, relaxed policies

### 3. Merge Metadata Tracking
Every merge creates metadata:
```json
{
  "merge_date": "2024-10-15T10:30:00Z",
  "source_projects": ["acme_corporate", "python_standards", "payment_gateway"],
  "overrides_applied": {...}
}
```

### 4. Version Control
Merged projects are versioned:
- `payment_gateway_prod_v1_0_0`
- `payment_gateway_prod_v1_1_0`

## Integration with Examples

This repository is used by:
- `/examples/corporate_sdlc/` - Corporate SDLC demo
- `/mcp_service/examples/` - MCP service examples
- `/mcp_service/tests/` - MCP service tests

## Adding New Projects

To add a new project:

1. Create directory structure:
```bash
mkdir -p example_projects_repo/my_project/config
```

2. Create `project.json`:
```json
{
  "id": "my_project",
  "name": "My Project",
  "description": "Project description",
  "created_at": "2024-10-15T10:00:00Z"
}
```

3. Create `config/config.yml`:
```yaml
system:
  name: my_project
  settings:
    key: value
```

4. Update `projects.json` registry

## Related Documentation

- [MCP Service README](../mcp_service/README.md)
- [Corporate SDLC Example](../examples/corporate_sdlc/)
- [Architecture Documentation](../ARCHITECTURE.md)
- [Usage Examples](../USAGE_EXAMPLES.md)
