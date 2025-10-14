# Task Template

Use this template for tracking tasks in `claude_tasks/active/ACTIVE_TASKS.md`

## Template

```markdown
### Task #N: [Title]
- **Priority**: [High/Medium/Low]
- **Status**: [Not Started/In Progress/Blocked/Completed]
- **Assigned**: [Name or "Unassigned"]
- **Created**: [Date]
- **Due**: [Date or "None"]

#### Description
[Clear description of what needs to be done]

#### Behavior/Scenario (BDD)
[Link to Gherkin scenario if applicable]
```gherkin
Feature: [Feature name]
Scenario: [Scenario name]
  Given [context]
  When [action]
  Then [expected result]
```

#### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

#### Technical Notes
- [Implementation details]
- [Dependencies]
- [Risks/Concerns]

#### Tests
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] All tests passing
- [ ] Coverage > 80%

#### Documentation
- [ ] Code comments
- [ ] README updated
- [ ] API docs updated
- [ ] Examples provided

#### Related
- Related to: [Task #X]
- Blocked by: [Task #Y]
- Blocks: [Task #Z]
```

## Example

```markdown
### Task #1: Add Config Validation
- **Priority**: High
- **Status**: In Progress
- **Assigned**: Claude
- **Created**: 2024-10-15
- **Due**: 2024-10-16

#### Description
Add validation to ensure all required config fields are present
and have correct types when loading configuration.

#### Behavior/Scenario (BDD)
```gherkin
Feature: Configuration Validation
Scenario: Load valid configuration
  Given a YAML file with all required fields
  When I load the configuration
  Then it should load successfully

Scenario: Load invalid configuration
  Given a YAML file missing required fields
  When I load the configuration
  Then it should raise a ValidationError
```

#### Acceptance Criteria
- [ ] Validates required fields exist
- [ ] Validates field types match schema
- [ ] Provides clear error messages
- [ ] All edge cases tested

#### Technical Notes
- Use jsonschema for validation
- Define schema in separate file
- Support custom validators

#### Tests
- [ ] Unit tests for each validation rule
- [ ] Integration test with real config
- [ ] Error message tests
- [ ] Coverage > 90%

#### Documentation
- [ ] Add docstrings to validator functions
- [ ] Update README with validation info
- [ ] Add example of validation error

#### Related
- Related to: Task #2 (Config Loading)
- Blocks: Task #3 (Config Merging)
```

---

*Use this template to keep tasks organized and trackable*
