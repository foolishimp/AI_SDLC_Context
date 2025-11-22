Display the current AI SDLC project status by analyzing `.ai-workspace/` tasks and project artifacts.

## Instructions

Execute the following analysis and display results:

### 1. Check Intent
- **Read** `INTENT.md` (if exists)
- **Display**: "📄 Intent: ✅ INTENT.md exists ({size} bytes)" or "❌ INTENT.md missing"

### 2. Analyze Stage Completion

**Stage 1 (Requirements):**
- **Check**: `docs/requirements/` directory exists and contains files
- **Count**: REQ-* keys using `grep -r "REQ-F-\|REQ-NFR-\|REQ-DATA-\|REQ-BR-" docs/requirements/`
- **Status**: ✅ Complete if files exist, ❌ TODO if not

**Stage 2 (Design):**
- **Check**: `docs/design/` directory exists and contains files
- **Count**: Traceability tags using `grep -r "→ REQ-\|Implements: REQ-" docs/design/`
- **List**: Design document names
- **Status**: ✅ Complete if files exist, ❌ TODO if not

**Stage 3 (Tasks):**
- **Read**: `.ai-workspace/tasks/active/ACTIVE_TASKS.md`
- **Count**: Active tasks (look for "## Task #" headers)
- **List**: Recently finished from `.ai-workspace/tasks/finished/` (last 5 files)
- **Read**: `.ai-workspace/tasks/todo/TODO_LIST.md`
- **Count**: TODO items
- **Status**: ✅ Complete if no active tasks, ⚠️ In Progress if has active, ❌ TODO if empty

**Stage 4 (Code):**
- **Check**: `src/` or `installers/` or `mcp_service/` or `plugins/` directories exist
- **Check**: `tests/` directory exists
- **Check**: `.coverage` file exists (run `coverage report --format=total` if available)
- **Status**: ✅ Complete if coverage ≥80%, ⚠️ In Progress if <80%, ❌ TODO if no code

**Stage 5 (System Test):**
- **Check**: `tests/bdd/` directory exists
- **Count**: `*.feature` files if directory exists
- **Status**: ✅ Complete if scenarios exist and passing, ❌ TODO if not

**Stage 6 (UAT):**
- **Check**: `docs/uat/` directory exists
- **Check**: Sign-off documents using `grep -r "Sign-off.*Approved" docs/uat/`
- **Status**: ✅ Complete if sign-off exists, ❌ TODO if not

**Stage 7 (Runtime Feedback):**
- **Check**: `docs/releases/` directory exists or deployment evidence
- **Status**: ✅ Complete if deployed, ❌ TODO if not

### 3. Display Session Context (if exists)

- **Check**: `.ai-workspace/session/current_session.md` exists
- **Read**: Extract session goals if file exists
- **Display**: Current session info or "No active session"

### 4. Generate Summary

Display in this format:

```
╔══════════════════════════════════════════════════════════════╗
║        AI SDLC Project Status: {project_name}                ║
╚══════════════════════════════════════════════════════════════╝

📄 Intent: {status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Stage 1: Requirements                                    {status}
   {artifacts list}

🎨 Stage 2: Design                                          {status}
   {artifacts list}

📝 Stage 3: Tasks                                           {status}
   → Active: {count}
   → Finished: {count} (recent)
   → TODO: {count}

💻 Stage 4: Code                                            {status}
   {code directories}
   → Coverage: {percentage}%

🧪 Stage 5: System Test                                     {status}
🎯 Stage 6: UAT                                             {status}
📊 Stage 7: Runtime Feedback                                {status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Current Focus: {from session or active tasks}

📌 Next Steps:
   {top 5-7 items from TODO or inferred from gaps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Overall Progress: {X}/7 stages complete or in progress

✅ Completed: {list}
⚠️ In Progress: {list}
❌ Not Started: {list}

Recommendation: {next highest priority stage}
```

### 5. Quality Gate Checks

For each stage, note which quality gates are satisfied:

- **Requirements**: All requirements have unique keys? Acceptance criteria?
- **Design**: All components mapped to requirements (100% traceability)?
- **Tasks**: All tasks linked to requirement keys? All estimated?
- **Code**: All code has tests? Coverage ≥80%? All tests passing?
- **System Test**: All requirements have ≥1 BDD scenario? Coverage ≥95%?
- **UAT**: Business sign-off obtained?
- **Runtime Feedback**: Deployed with telemetry?

---

**Note**: This command is read-only and analyzes project state without modifying files.
