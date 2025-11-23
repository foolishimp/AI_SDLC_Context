# AI SDLC Context Refresh for Claude

**Version:** 2.0.0
**Purpose:** Load this to refresh Claude's context with AI SDLC methodology
**When to use:** Start of session, after context loss, before any work, after violations

---

## 🎯 Core Principle

**"No work without task tracking. No task without documentation."**

**How to use this document:**
1. Read at start of every session
2. Read after making mistakes
3. Read when unsure of workflow
4. Reference quick cards at bottom for fast lookup

---

## 📁 Workspace Structure (NEVER VIOLATE THIS!)

```
.ai-workspace/
├── tasks/
│   ├── todo/
│   │   └── TODO_LIST.md           # Quick capture (informal)
│   ├── active/
│   │   └── ACTIVE_TASKS.md        # Formal tasks (TDD required)
│   └── finished/                  # Completed task documentation
│       └── YYYYMMDD_HHMM_task_name.md
│
├── session/
│   └── current_session.md         # Active session tracking
│
├── templates/                     # Templates for tasks/sessions
└── config/                        # Workspace configuration
```

**CRITICAL RULES:**
- ✅ **DO**: Put finished tasks in `.ai-workspace/tasks/finished/`
- ❌ **DON'T**: Put tasks in `docs/`, `finished_tasks/`, or anywhere else
- ✅ **DO**: Use `TodoWrite` tool for task tracking
- ❌ **DON'T**: Create task files manually without following workflow

---

## 🔄 Proper Workflow (ALWAYS FOLLOW THIS!)

### Session Start
```bash
/aisdlc-start-session
# Claude prompts for:
# - Primary goal (must complete)
# - Secondary goal (should complete)
# - Working mode (TDD / Bug Fix / Exploration)
# - Check-in frequency (15 or 30 minutes)
```

### During Work
```bash
# Quick capture
/aisdlc-todo "description"

# Use TodoWrite tool to track progress
# (Claude should proactively use this!)
```

### After Work
```bash
/aisdlc-checkpoint-tasks
# Claude will:
# - Review conversation history
# - Evaluate active tasks
# - Create finished task docs in CORRECT location
# - Update ACTIVE_TASKS.md
# - Provide summary report
```

### Commit
```bash
/aisdlc-commit-task <id>
# Generates proper commit message with REQ tags
```

---

## 🛠️ Tools to Use (Claude's Toolkit)

### Task Tracking
- **`TodoWrite` tool** - Track task progress in real-time
  - Use proactively during work
  - Update status: pending → in_progress → completed

### Slash Commands
- `/aisdlc-start-session` - Begin session
- `/aisdlc-todo "desc"` - Quick capture
- `/aisdlc-checkpoint-tasks` - Sync tasks with reality ⭐ **USE AFTER WORK**
- `/aisdlc-finish-task <id>` - Complete specific task
- `/aisdlc-commit-task <id>` - Generate commit message
- `/aisdlc-status` - Show 7-stage SDLC status

### File Operations
- **Read** - Read existing files
- **Write** - Create new files (use sparingly!)
- **Edit** - Modify existing files (preferred)
- **Bash** - Git operations, tests, builds

---

## 📋 Task Lifecycle

### 1. Quick Todo (Informal)
```markdown
Location: .ai-workspace/tasks/todo/TODO_LIST.md
Command: /aisdlc-todo "description"
Purpose: Capture thoughts without breaking flow
```

### 2. Active Task (Formal)
```markdown
Location: .ai-workspace/tasks/active/ACTIVE_TASKS.md
Required:
- Task ID
- Priority (High/Medium/Low)
- Status (Not Started/In Progress/Blocked)
- Acceptance Criteria
- Feature Flag (if code)
- Requirement Traceability (REQ-*)

TDD Required: YES (unless documentation task)
```

### 3. Finished Task (Documentation)
```markdown
Location: .ai-workspace/tasks/finished/YYYYMMDD_HHMM_task_name.md
Template: .ai-workspace/templates/FINISHED_TASK_TEMPLATE.md
Required Sections:
- Problem
- Investigation
- Solution
- TDD Process (if code)
- Files Modified
- Test Coverage (if code)
- Result
- Traceability
- Metrics
- Lessons Learned
```

---

## 🎨 The 7 Key Principles (Code Stage)

**Full details:** `plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md`

1. **Test Driven Development** - RED → GREEN → REFACTOR → COMMIT
2. **Fail Fast & Root Cause** - Fix at source, no workarounds
3. **Modular & Maintainable** - Single responsibility
4. **Reuse Before Build** - Check existing first
5. **Open Source First** - Suggest alternatives
6. **No Legacy Baggage** - Start clean
7. **Perfectionist Excellence** - Excellence or nothing 🔥

**TDD Workflow:** `plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md`

---

## 🎯 7-Stage AI SDLC

**Full details:** `docs/ai_sdlc_method.md` (3,300+ lines)
**Agent configs:** `plugins/aisdlc-methodology/config/stages_config.yml` (1,273 lines)

```
Intent → Requirements → Design → Tasks → Code → System Test → UAT → Runtime Feedback
           ↑                                                                   ↓
           └────────────────────── Feedback Loop ─────────────────────────────┘
```

**Quick stage reference:**
1. Requirements → REQ-F-*, REQ-NFR-*, REQ-DATA-*
2. Design → Components, APIs, ADRs
3. Tasks → Jira tickets with REQ tags
4. **Code** → TDD (RED→GREEN→REFACTOR), tag with `# Implements: REQ-*` ⭐ **PRIMARY**
5. System Test → BDD (Given/When/Then)
6. UAT → Business validation
7. Runtime Feedback → Telemetry → new intents

**Use `/aisdlc-status` to see current stage**

---

## ⚠️ Common Violations (DON'T DO THESE!)

### ❌ Task Location Violations
```
WRONG: docs/finished_tasks/task.md
WRONG: finished_tasks/task.md
WRONG: tasks/task.md
RIGHT: .ai-workspace/tasks/finished/YYYYMMDD_HHMM_task.md
```

### ❌ Workflow Violations
```
WRONG: Start work immediately without task
WRONG: Finish work without /aisdlc-checkpoint-tasks
WRONG: Create task files manually
RIGHT: /aisdlc-start-session → work → /aisdlc-checkpoint-tasks
```

### ❌ Tool Violations
```
WRONG: Don't use TodoWrite tool
WRONG: Manually create finished task files
WRONG: Skip slash commands
RIGHT: Use TodoWrite, use /aisdlc-checkpoint-tasks, follow workflow
```

---

## ✅ Pre-Flight Checklist (Before Starting ANY Work)

1. [ ] Have I run `/aisdlc-start-session`?
2. [ ] Is there a task in `ACTIVE_TASKS.md`?
3. [ ] Am I using `TodoWrite` tool to track progress?
4. [ ] Do I know which stage I'm in (Requirements/Design/Code/etc.)?
5. [ ] Have I read this reference document?

**If ANY answer is "no", STOP and correct before proceeding.**

---

## 🚨 Recovery from Violations

### If you violated workspace structure:
1. **STOP** immediately
2. Acknowledge violation to user
3. Move/delete incorrectly placed files
4. Create files in CORRECT location
5. Update this reference if needed

### If you violated workflow:
1. **STOP** and acknowledge
2. Run `/aisdlc-checkpoint-tasks`
3. Properly document work retroactively
4. Learn from violation

### If you're unsure:
1. **ASK** the user before proceeding
2. Reference this document
3. Check `.ai-workspace/` structure
4. Use slash commands

---

## 📚 Quick Reference Card

### File Locations
| What | Where |
|------|-------|
| Quick todos | `.ai-workspace/tasks/todo/TODO_LIST.md` |
| Active tasks | `.ai-workspace/tasks/active/ACTIVE_TASKS.md` |
| Finished tasks | `.ai-workspace/tasks/finished/YYYYMMDD_HHMM_*.md` |
| Session tracking | `.ai-workspace/session/current_session.md` |
| Templates | `.ai-workspace/templates/` |

### Commands
| When | Command |
|------|---------|
| Start session | `/aisdlc-start-session` |
| Quick capture | `/aisdlc-todo "desc"` |
| After work | `/aisdlc-checkpoint-tasks` ⭐ |
| Finish task | `/aisdlc-finish-task <id>` |
| Commit | `/aisdlc-commit-task <id>` |
| Check stage | `/aisdlc-status` |

### TDD Cycle
```
RED    → Write failing test first
GREEN  → Implement minimal solution
REFACTOR → Improve code quality
COMMIT → Save with REQ tags
```

---

## 🎓 Learning from Common Violations

**Violation: Started work without session setup**
- ❌ Started coding immediately
- ✅ Should: `/aisdlc-start-session` → add to ACTIVE_TASKS.md → work

**Violation: Put finished task in wrong location**
- ❌ Created in `docs/finished_tasks/`
- ✅ Should: `.ai-workspace/tasks/finished/YYYYMMDD_HHMM_*.md`

**Violation: Forgot to track progress**
- ❌ Didn't use TodoWrite tool during work
- ✅ Should: Use TodoWrite proactively to track progress

**Violation: Forgot to checkpoint**
- ❌ Finished work without `/aisdlc-checkpoint-tasks`
- ✅ Should: Always checkpoint after work to sync docs

**Key Takeaways:**
1. Load this document at session start
2. Use `/aisdlc-checkpoint-tasks` after ANY work
3. Never create files manually - use commands/tools
4. When in doubt, ASK before proceeding

---

**Version:** 2.0.0
**Last Updated:** 2025-11-23
**Maintained By:** AI SDLC Method Team

**"Excellence or nothing"** 🔥
