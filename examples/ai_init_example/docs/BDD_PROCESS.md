# BDD Process - 9-Step Enhanced Methodology

This document describes the Behavior-Driven Development process used by AI Init.

## The 9 Steps

### Phase 1: Specification (BDD)
**Step 1: SPECIFY** - Write Gherkin behavior scenarios
- Define user stories and acceptance criteria
- Write scenarios in `claude_tasks/behaviors/features/`
- Collaborate with stakeholders
- Focus on business value

**Step 2: COLLABORATE** - Review with stakeholders
- Validate scenarios with business
- Ensure shared understanding
- Document assumptions
- Get stakeholder sign-off

### Phase 2: Implementation (TDD)
**Step 3: RED** - Write failing tests from scenarios
- Convert Gherkin steps to test cases
- Implement step definitions
- Run tests (should fail)
- Verify test quality

**Step 4: GREEN** - Write minimal code to pass
- Implement just enough code
- Focus on making tests pass
- Don't optimize yet
- Verify all tests pass

**Step 5: REFACTOR** - Improve code quality
- Enhance design
- Remove duplication
- Improve readability
- Keep tests green

### Phase 3: Validation (BDD)
**Step 6: VALIDATE** - Confirm behavior works
- Run full test suite
- Execute scenarios end-to-end
- Verify acceptance criteria
- Check edge cases

**Step 7: DOCUMENT** - Generate living documentation
- Create behavior reports
- Update scenario status
- Document decisions
- Share with stakeholders

**Step 8: DEMO** - Show working software
- Demonstrate to stakeholders
- Collect feedback
- Validate assumptions
- Update scenarios if needed

**Step 9: ITERATE** - Refine based on feedback
- Incorporate feedback
- Update scenarios
- Adjust implementation
- Return to Step 1 for next feature

## Quick Workflow

```
SPECIFY → COLLABORATE → RED → GREEN → REFACTOR → VALIDATE → DOCUMENT → DEMO → ITERATE
   ↓          ↓         ↓      ↓        ↓          ↓          ↓        ↓       ↓
Scenario → Review → Fail → Pass → Clean → Verify → Report → Show → Next
```

## Example

### Step 1: SPECIFY
```gherkin
Feature: Claude Task Management
  As a developer
  I want to track tasks with Claude
  So that I can maintain project clarity

Scenario: Create new task
  Given I have an empty active tasks file
  When I create a new task "Implement feature X"
  Then the task should appear in active tasks
  And the task should have status "Not Started"
```

### Step 2: COLLABORATE
- Review with team lead
- Confirm "active tasks file" location
- Agree on status values
- Document in scenario

### Steps 3-5: TDD Cycle
- Write test for scenario
- Implement minimal code
- Refactor

### Steps 6-9: Validation
- Run scenarios
- Generate report
- Demo to stakeholders
- Iterate

---

This process ensures code meets real business needs while maintaining technical quality.
