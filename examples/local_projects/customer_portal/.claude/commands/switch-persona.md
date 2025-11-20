# Switch Persona

Switch from one persona to another and see what changed in focus areas.

## Usage

```
/switch-persona <new-persona-name>
```

## Example

```bash
# Switch from engineer to QA
/switch-persona qa_engineer

# Claude reports:
# Switched from software_engineer to qa_engineer
#
# Added Focus Areas:
#   ✚ Test planning
#   ✚ Test automation
#   ✚ Quality assurance
#
# Removed Focus Areas:
#   ✖ Code implementation
#   ✖ Technical design
```

## Use Cases

**During Code Review:**
```bash
# Start with engineer perspective
/apply-persona software_engineer
# Review code quality...

# Switch to security perspective
/switch-persona security_engineer
# Review security issues...

# Switch to DevOps perspective
/switch-persona devops_engineer
# Review deployability...
```

## See Also

- `/apply-persona` - Apply initial persona
- `/list-personas` - See all personas
- `/persona-checklist` - Get review checklist
