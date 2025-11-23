Checkpoint active tasks against current conversation context and update their status.

**Usage**: `/aisdlc-checkpoint-tasks`

**Instructions**:

## Phase 0: Refresh AI SDLC Context

**CRITICAL**: Before proceeding, refresh Claude's context with the AI SDLC methodology:

1. **Read** `.ai-workspace/templates/AISDLC_METHOD_REFERENCE.md`
   - This loads workspace structure rules
   - This loads workflow patterns
   - This loads violation warnings
   - This ensures correct file locations

2. **Confirm understanding**:
   - Finished tasks go in: `.ai-workspace/tasks/finished/`
   - Active tasks are in: `.ai-workspace/tasks/active/ACTIVE_TASKS.md`
   - Never put tasks in `docs/` or anywhere else

**Why this matters**: Without context refresh, Claude may violate workspace structure rules and create files in wrong locations.

---

## Phase 1: Analyze Current Context
1. **Review conversation history** to identify:
   - What work has been completed recently
   - What files were modified
   - What tests were run and their results
   - What commits were made
   - Any side tasks or tangential work done

## Phase 2: Evaluate Active Tasks
1. **Read** `.ai-workspace/tasks/active/ACTIVE_TASKS.md`
2. **For each active task**, determine:
   - **Completed**: All acceptance criteria met, tests passing, documented
   - **In Progress**: Work has started, some acceptance criteria met
   - **Blocked**: Dependencies not met or blockers encountered
   - **Not Started**: No evidence of work in current context
   - **Partially Relevant**: Side work relates to this task

## Phase 3: Update Task Status
For each task, perform appropriate action:

### For COMPLETED tasks:
1. **Read** `.ai-workspace/templates/FINISHED_TASK_TEMPLATE.md`
2. **Create** finished task document:
   - Path: `.ai-workspace/tasks/finished/{YYYYMMDD_HHMM}_{task_slug}.md`
   - Fill all sections based on conversation context:
     - Problem: Original task description
     - Investigation: What was discovered during work
     - Solution: How it was solved
     - TDD Process: RED/GREEN/REFACTOR phases (if applicable)
     - Files Modified: Extract from conversation (git commits, edits, writes)
     - Test Coverage: Extract from test runs in conversation
     - Code Changes: Relevant before/after snippets
     - Testing: Commands run and results
     - Result: Final outcome
     - Traceability: REQ-* keys from task
     - Metrics: Estimate based on changes
   - **Note**: If documentation task, adapt sections appropriately
3. **Remove** completed task from `ACTIVE_TASKS.md`
4. Log: "✅ Task #{id} completed and archived"

### For IN PROGRESS tasks:
1. **Update** status in `ACTIVE_TASKS.md`:
   - Change status from "Not Started" to "In Progress"
   - Add progress notes with what has been done
   - Update acceptance criteria checkboxes based on completion
   - Add any blockers or dependencies discovered
2. Log: "🔄 Task #{id} status updated to In Progress"

### For BLOCKED tasks:
1. **Update** status in `ACTIVE_TASKS.md`:
   - Change status to "Blocked"
   - Document blocker reason
   - Note dependencies or required actions
2. Log: "🚫 Task #{id} marked as Blocked"

### For NOT STARTED tasks:
1. **No changes** - leave as is
2. Log: "⏸️  Task #{id} not started (no changes)"

## Phase 4: Summary Report
Provide a summary in this format:

```
╔══════════════════════════════════════════════════════════════╗
║              Task Checkpoint - {YYYY-MM-DD HH:MM}            ║
╚══════════════════════════════════════════════════════════════╝

📊 Evaluation Summary:
   ✅ Completed: {count} task(s)
   🔄 In Progress: {count} task(s)
   🚫 Blocked: {count} task(s)
   ⏸️  Not Started: {count} task(s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Completed Tasks:
   {list completed task IDs and titles with archive paths}

🔄 In Progress:
   {list in-progress task IDs, titles, and what was done}

🚫 Blocked:
   {list blocked task IDs, titles, and blocker reasons}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Files Updated:
   - .ai-workspace/tasks/active/ACTIVE_TASKS.md
   {- .ai-workspace/tasks/finished/YYYYMMDD_HHMM_task_name.md (for each completed)}

💡 Next Steps:
   {suggestion based on remaining active tasks}
```

---

**Notes**:
- This command is particularly useful after side tasks or long work sessions
- It helps maintain accurate task state based on actual work done
- Use before `/aisdlc-status` to get accurate status
- The command uses conversation context, so ensure relevant work is in current context
- For ambiguous cases, ask the user for clarification before marking as completed

**Example Use Cases**:
- After working on a side task, checkpoint to see if any active tasks were incidentally completed
- At end of work session to update all task statuses
- Before context switch to ensure task state is accurate
- After a series of commits to update task progress
