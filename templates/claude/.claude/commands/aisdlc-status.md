# AI SDLC Project Status

Display current AI SDLC stage progress by analyzing `.ai-workspace/` tasks and project artifacts.

## Usage

```
/aisdlc-status
```

## What It Shows

**From `.ai-workspace/`:**
- Currently active work (Stage 3 - Tasks)
- Recently finished tasks
- Next steps from TODO list
- Session goals and progress

**From Project Structure:**
- Intent status (INTENT.md exists?)
- Stage completion inference (based on artifacts)
- Quality gate status per stage
- Requirement traceability coverage

## Status Inference Logic

The command analyzes the project following the AI SDLC methodology:

### Intent Status
```
✅ INTENT.md exists → Project has clear business intent
❌ Missing → Need to create INTENT.md at project root
```

### Stage 1: Requirements
```
Check: docs/requirements/ for REQ-* keys
✅ Complete: Requirements files exist with REQ-F-*, REQ-NFR-*, etc.
⚠️ In Progress: Some requirements defined
❌ TODO: No requirements documents
```

### Stage 2: Design
```
Check: docs/design/ for design artifacts
✅ Complete: Design docs exist with requirement traceability (→ REQ-*)
⚠️ In Progress: Design docs exist but incomplete traceability
❌ TODO: No design documents
```

### Stage 3: Tasks
```
Check: .ai-workspace/tasks/
✅ Complete: No active tasks, all finished
⚠️ In Progress: X active tasks, Y finished tasks
❌ TODO: No tasks defined
```

### Stage 4: Code
```
Check: src/, tests/, test coverage
✅ Complete: Code exists, tests passing, coverage ≥80%
⚠️ In Progress: Code exists, coverage <80%
❌ TODO: No source code
```

### Stage 5: System Test
```
Check: tests/bdd/ for BDD scenarios
✅ Complete: BDD scenarios exist and passing
⚠️ In Progress: BDD scenarios exist, some failing
❌ TODO: No BDD scenarios
```

### Stage 6: UAT
```
Check: docs/uat/ for business sign-off
✅ Complete: UAT complete with sign-off
⚠️ In Progress: UAT test cases exist, no sign-off
❌ TODO: No UAT artifacts
```

### Stage 7: Runtime Feedback
```
Check: docs/releases/ or production deployment
✅ Complete: Deployed with telemetry
⚠️ In Progress: Deployed but no telemetry
❌ TODO: Not deployed
```

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║           AI SDLC Project Status: ai_sdlc_method             ║
╚══════════════════════════════════════════════════════════════╝

📄 Intent: ✅ INTENT.md exists (10,447 bytes)
   "Build AI SDLC methodology for AI-augmented development"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Stage 1: Requirements                                    ✅ COMPLETE
   → docs/requirements/FOLDER_BASED_REQUIREMENTS.md
   Quality Gates: All requirements documented

🎨 Stage 2: Design                                          ✅ COMPLETE
   → docs/design/AI_SDLC_UX_DESIGN.md (1,400 lines)
   → docs/design/CLAUDE_AGENTS_EXPLAINED.md
   → docs/design/FOLDER_BASED_ASSET_DISCOVERY.md
   → docs/design/AGENTS_SKILLS_INTEROPERATION.md
   Quality Gates: Design artifacts exist with traceability

📝 Stage 3: Tasks                                           ⚠️ IN PROGRESS
   → Active Tasks: 3
      • Fix plugin installer non-interactive mode
      • Create config/config.yml for this project
      • Add BDD tests for installers
   → Recently Finished: 5
      • Dogfood AI SDLC structure
      • Create INTENT.md
      • Reorganize docs/ by stage
      • Setup data_mapper.test02
      • Install AI SDLC workspace
   → TODO List: 8 items
   Quality Gates: Tasks tracked in .ai-workspace/

💻 Stage 4: Code                                            ⚠️ IN PROGRESS
   → installers/ (3 scripts)
   → mcp_service/ (implemented)
   → plugins/ (9 plugins)
   → Test Coverage: 78% (target: ≥80%)
   Quality Gates: Need to increase test coverage

🧪 Stage 5: System Test                                     ❌ TODO
   → tests/bdd/ directory missing
   → No BDD scenarios defined
   Quality Gates: Need ≥1 BDD scenario per requirement

✓ Stage 6: UAT                                              ❌ TODO
   → docs/uat/ directory missing
   → No UAT test cases
   Quality Gates: Need business sign-off

📊 Stage 7: Runtime Feedback                                ❌ TODO
   → Not deployed to production
   → No telemetry configured
   Quality Gates: Need deployment + telemetry

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Current Focus (from .ai-workspace/session/):
   Session started: 2025-01-22 18:00
   Goals:
   • Complete Code stage (reach 80% coverage)
   • Create BDD test scenarios
   • Document current project status

📌 Next Steps:
   1. Fix plugin installer (enable non-interactive mode)
   2. Write BDD scenarios for installer scripts
   3. Increase test coverage to 80%
   4. Create config/config.yml with 7-stage configuration
   5. Define UAT criteria for internal validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Overall Progress: 4/7 stages complete or in progress

✅ Completed: Intent, Requirements, Design
⚠️ In Progress: Tasks (3 active), Code (78% coverage)
❌ Not Started: System Test, UAT, Runtime Feedback

Recommendation: Focus on completing Code stage (increase coverage),
then move to System Test stage (create BDD scenarios).
```

## Implementation Details

The command should:

1. **Read from `.ai-workspace/`:**
   - Parse `.ai-workspace/tasks/active/ACTIVE_TASKS.md` for current work
   - List recent tasks from `.ai-workspace/tasks/finished/`
   - Read `.ai-workspace/tasks/todo/TODO_LIST.md` for next steps
   - Check `.ai-workspace/session/current_session.md` for session goals

2. **Scan Project Structure:**
   - Check `INTENT.md` existence and size
   - Count files in `docs/requirements/`, `docs/design/`, etc.
   - Check for REQ-* keys in requirements
   - Check for traceability tags (→ REQ-) in design
   - Detect `src/`, `tests/` directories
   - Run coverage report if available
   - Check for `tests/bdd/` directory
   - Check for `docs/uat/` directory
   - Check for `docs/releases/` or deployment evidence

3. **Infer Quality Gates:**
   - Requirements: REQ-* keys exist?
   - Design: Traceability tags exist?
   - Tasks: Active vs finished ratio
   - Code: Test coverage percentage
   - System Test: BDD scenarios exist?
   - UAT: Sign-off documentation exists?
   - Runtime Feedback: Deployment evidence?

4. **Output Format:**
   - Clear visual hierarchy (boxes, lines)
   - Status icons: ✅ Complete, ⚠️ In Progress, ❌ TODO
   - Actionable next steps
   - Overall progress summary

## Files Analyzed

```
Project Root:
├── INTENT.md                      # Intent status
├── docs/
│   ├── requirements/              # Stage 1 artifacts
│   ├── design/                    # Stage 2 artifacts
│   └── uat/                       # Stage 6 artifacts
├── .ai-workspace/
│   ├── tasks/
│   │   ├── active/                # Stage 3 current work ⭐
│   │   ├── finished/              # Stage 3 completed work ⭐
│   │   └── todo/                  # Stage 3 backlog ⭐
│   └── session/
│       └── current_session.md     # Current session goals ⭐
├── src/                           # Stage 4 code
├── tests/                         # Stage 4 tests
│   └── bdd/                       # Stage 5 BDD scenarios
└── docs/releases/                 # Stage 7 deployment artifacts
```

## Configuration

The command respects `.ai-workspace/config/workspace_config.yml` for:
- Quality gate thresholds (e.g., coverage target)
- Stage completion criteria overrides
- Custom artifact locations

## See Also

- `/start-session` - Begin development session with goals
- `/todo "task"` - Add to TODO list
- `/finish-task <id>` - Mark task complete
- `/current-context` - Show loaded project context
- `cat .ai-workspace/tasks/active/ACTIVE_TASKS.md` - View active tasks
- `cat .ai-workspace/tasks/finished/` - View completed tasks
- `cat INTENT.md` - View project intent

## Notes

- This command is **read-only** - it analyzes but doesn't modify
- Status is inferred from artifacts - keep `.ai-workspace/` up to date
- For requirement-level detail, check `docs/TRACEABILITY_MATRIX.md` (if exists)
- The command follows the AI SDLC methodology defined in `docs/methodology/ai_sdlc_method.md`

---

**Prefix:** `aisdlc-*` commands follow AI SDLC methodology conventions
