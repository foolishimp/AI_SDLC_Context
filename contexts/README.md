# Baseline Contexts

This directory contains **baseline contexts** provided by AI_SDLC_Context. These are read-only reference contexts that can be used as the foundation for your projects.

## Available Contexts

### aisdlc_methodology/
**Type**: Methodology
**Description**: Core development methodology - Sacred Seven principles and TDD workflow
**Depends on**: None (foundation)

**What it provides**:
- Sacred Seven development principles
- TDD workflow (RED → GREEN → REFACTOR)
- Pair programming practices
- Session management guides
- Task documentation templates
- Quality standards and enforcement

**When to use**: Include as the base layer in every context tuple

---

### python_standards/
**Type**: Language Standards
**Description**: Python-specific coding standards and best practices
**Depends on**: `aisdlc_methodology`

**What it provides**:
- PEP 8 style guidelines
- Python-specific testing practices (pytest)
- Type hints and documentation standards
- Python tooling configuration (black, mypy, pylint)
- Python project structure
- Package management best practices

**When to use**: Include when developing Python projects

---

## Usage

### In a Context Tuple

```json
{
  "context_tuple": [
    "corporate.aisdlc_methodology",
    "corporate.python_standards",
    "local.my_project"
  ]
}
```

### Server Configuration

When running an MCP context server, point to this directory:

```bash
python -m mcp_service.server \
  --port 8000 \
  --contexts-dir /path/to/AI_SDLC_Context/contexts
```

The server will automatically discover and serve all contexts defined in `contexts.json`.

---

## See Also

- [Example Projects](../examples/) - How to use and customize baseline contexts
- [MCP Service Docs](../mcp_service/docs/) - Running context servers
