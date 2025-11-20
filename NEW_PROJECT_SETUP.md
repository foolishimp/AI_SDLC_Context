# Setting Up a New Project with AI SDLC Method

**Scenario**: You have `ai_sdlc_method` on your local disk and want to start a new project in a different folder.

---

## Prerequisites

- ✅ AI SDLC Method repository: `/Users/jim/src/apps/ai_sdlc_method`
- ✅ Claude Code installed
- ✅ New project location: e.g., `/path/to/my-new-project`

---

## Step-by-Step Setup

### Step 1: Install Plugins Globally (One-Time Setup)

**Do this ONCE** - plugins will be available to all your future projects.

```bash
# Navigate to ai_sdlc_method
cd /Users/jim/src/apps/ai_sdlc_method

# Install startup bundle (recommended) or enterprise (complete)
python installers/setup_plugins.py --global --bundle startup

# OR install enterprise bundle for full suite
python installers/setup_plugins.py --global --bundle enterprise
```

**Verify installation**:
```bash
ls ~/.config/claude/plugins/
# Should see: aisdlc-core, aisdlc-methodology, principles-key (+ more if enterprise)
```

✅ **You only need to do this once!** Plugins are now available to all projects.

---

### Step 2: Create Your New Project Directory

```bash
# Create and navigate to your new project
mkdir -p /path/to/my-new-project
cd /path/to/my-new-project

# Initialize git (recommended)
git init
```

---

### Step 3: Install AI SDLC Development Tools

Run the installer from your local ai_sdlc_method:

```bash
# Install workspace + commands (plugins already installed globally)
python /Users/jim/src/apps/ai_sdlc_method/installers/setup_all.py

# This installs:
# - .ai-workspace/ (task tracking, session management)
# - .claude/commands/ (slash commands: /todo, /start-session, etc.)
# - CLAUDE.md (project guidance)
# - .gitignore (configured for workspace)
```

**Output**:
```
✅ Developer Workspace (.ai-workspace/)
✅ Claude Commands (.claude/commands/)
✅ .gitignore updates
✅ CLAUDE.md
```

---

### Step 4: Create Your Project Intent

Create an intent file describing what you want to build:

```bash
# Create INTENT.md
cat > INTENT.md <<'EOF'
# Intent: [Your Project Name]

**Intent ID**: INT-001
**Date**: 2025-01-21
**Product Owner**: your-name@company.com
**Priority**: High

---

## User Story

As a [type of user], I want to [do something] so that I can [achieve goal].

---

## Business Context

[Describe the business need, problem to solve, and why this matters]

**Business Value**:
- Benefit 1
- Benefit 2
- Benefit 3

**Success Metrics**:
- Metric 1: Target value
- Metric 2: Target value

---

## High-Level Requirements

1. **Feature 1**
   - Sub-requirement A
   - Sub-requirement B

2. **Feature 2**
   - Sub-requirement A
   - Sub-requirement B

---

## Out of Scope (This Intent)

- Thing 1
- Thing 2

---

## Constraints

- Constraint 1
- Constraint 2

---

## Dependencies

- Dependency 1
- Dependency 2

---

## Next Steps

This intent will flow through the 7-stage AI SDLC methodology.

---

**Status**: Ready for Requirements Stage
EOF
```

---

### Step 5: Create Project Configuration

Create a configuration file for your project:

```bash
# Create config directory
mkdir -p config

# Create project configuration
cat > config/config.yml <<'EOF'
project:
  name: My New Project
  team: Development Team
  tech_lead: your-name@company.com
  classification: internal

  description: |
    [Brief description of your project]

# ============================================================================
# AI SDLC METHODOLOGY - 7-STAGE CONFIGURATION
# ============================================================================

ai_sdlc:
  # Load 7-stage methodology from global plugins
  methodology_plugin: "~/.config/claude/plugins/aisdlc-methodology/config/stages_config.yml"
  principles_key: "~/.config/claude/plugins/principles-key/config/config.yml"

  # Enable stages you want to use
  enabled_stages:
    - requirements    # Generate REQ-* keys
    - design          # Technical solution
    - tasks           # Work breakdown
    - code            # TDD implementation
    - system_test     # BDD integration testing
    - uat             # Business validation
    - runtime_feedback # Production monitoring

  # Stage-specific configuration
  stages:
    requirements:
      personas:
        product_owner: your-po@company.com
        business_analyst: your-ba@company.com

      requirement_types:
        - type: functional
          prefix: REQ-F
        - type: non_functional
          prefix: REQ-NFR
        - type: data_quality
          prefix: REQ-DATA

      quality_gates:
        - all_requirements_have_unique_keys: true
        - all_requirements_have_acceptance_criteria: true

    code:
      testing:
        coverage_minimum: 80
        tdd_required: true

      principles_key:
        enabled: true
        enforce_tdd: true

    system_test:
      bdd:
        enabled: true
        framework: cucumber  # or: behave, jest-cucumber

      coverage_minimum: 90
EOF
```

---

### Step 6: Initial Git Commit

```bash
# Review what was created
ls -la

# Stage all files
git add .

# Initial commit
git commit -m "Initial project setup with AI SDLC Method

- Developer Workspace installed (.ai-workspace/)
- Claude commands installed (.claude/commands/)
- Project intent defined (INTENT.md)
- AI SDLC configuration (config/config.yml)
- Ready for 7-stage development process

🤖 Generated with [Claude Code](https://claude.ai/code)
"
```

---

### Step 7: Start Your First AI SDLC Session

```bash
# Start development session
# (This command works because you installed .claude/commands/)
/start-session
```

**Claude will prompt you for**:
- Primary goal (e.g., "Generate requirements from INTENT.md")
- Secondary goal
- Working mode (TDD / Exploration / etc.)

---

## Your Project Structure

After setup, your project should look like this:

```
my-new-project/
├── .ai-workspace/               # Developer Workspace
│   ├── README.md
│   ├── config/
│   │   └── workspace_config.yml
│   ├── tasks/
│   │   ├── todo/TODO_LIST.md
│   │   ├── active/ACTIVE_TASKS.md
│   │   ├── finished/
│   │   └── archive/
│   └── templates/
│
├── .claude/                     # Claude Code integration
│   ├── commands/                # Slash commands
│   │   ├── todo.md
│   │   ├── start-session.md
│   │   ├── finish-task.md
│   │   └── ... (10+ more)
│   └── hooks.json
│
├── config/
│   └── config.yml               # AI SDLC configuration
│
├── INTENT.md                    # Your project intent (INT-001)
├── CLAUDE.md                    # Project guidance
├── .gitignore                   # Git configuration
└── README.md                    # (Create this next)
```

---

## Running the 7-Stage AI SDLC Process

### Stage 1: Requirements

```
Ask Claude:

"Using the AI SDLC Requirements Stage configuration from config/config.yml,
generate structured requirements from INTENT.md.

Create:
1. REQ-F-* (functional requirements)
2. REQ-NFR-* (non-functional requirements)
3. REQ-DATA-* (data quality requirements)
4. Acceptance criteria for each
5. Traceability matrix"
```

**Expected Output**: `docs/requirements/REQUIREMENTS.md`

### Stage 2: Design

```
Ask Claude:

"Create technical solution for the requirements:
1. Component diagrams (Mermaid)
2. Data models
3. API specifications
4. Architecture decision records (ADRs)

Map each component to requirement keys."
```

**Expected Output**: Design docs in `docs/design/`

### Stage 3: Tasks

```
Ask Claude:

"Break the design into work items:
1. Create epic
2. Generate user stories
3. Create technical tasks
4. Add estimates and dependencies
5. Tag all items with requirement keys"
```

**Expected Output**: Work breakdown structure

### Stage 4: Code (TDD)

Follow TDD cycle:

```bash
# RED: Write failing test
npm test  # or: pytest

# GREEN: Implement minimal solution
npm test  # PASSES

# REFACTOR: Improve code quality
npm test  # STILL PASSES

# COMMIT: Save with REQ tags
/finish-task <id>
/commit-task <id>
```

### Stage 5: System Test (BDD)

```
Ask Claude:

"Create BDD integration tests:
1. Write feature files (Given/When/Then)
2. Implement step definitions
3. Validate all requirements
4. Achieve 90%+ coverage"
```

### Stage 6: UAT

```
Ask Claude:

"Create UAT test cases for business validation:
1. Manual test procedures
2. Automated UAT tests
3. Sign-off checklist"
```

### Stage 7: Runtime Feedback

```
Ask Claude:

"Set up production monitoring:
1. Tag all metrics with REQ keys
2. Configure alerts
3. Set up dashboards
4. Define feedback loop to new intents"
```

---

## Available Slash Commands

Once installed, you can use:

```bash
/todo "description"          # Quick capture a todo
/start-session               # Begin development session
/finish-task <id>            # Complete task with documentation
/commit-task <id>            # Generate commit message
/current-context             # Show current stage context
/load-context                # Load project configuration
```

---

## Common Workflows

### Daily Development

```bash
# Morning routine
cd /path/to/my-new-project
/start-session

# Capture thoughts during coding
/todo "add error handling to payment flow"
/todo "investigate slow query"

# Complete a task
/finish-task 5
/commit-task 5

# End of day
cat .ai-workspace/session/current_session.md  # Review progress
```

### Adding Features

```bash
# 1. Create new intent
cat > INTENT_002.md <<EOF
# Intent: New Feature Name
...
EOF

# 2. Start session
/start-session

# 3. Ask Claude to run through 7 stages
# Stage 1: Requirements
# Stage 2: Design
# ... etc
```

### Bug Fixes

```bash
# 1. Document the bug as an intent
cat > INTENT_BUG_001.md <<EOF
# Intent: Fix authentication timeout bug
...
EOF

# 2. Follow TDD for bug fix
# - Write test that reproduces bug (RED)
# - Fix bug (GREEN)
# - Refactor (REFACTOR)
# - Commit with REQ tags
```

---

## Tips & Best Practices

### 1. **Start Small**
Don't enable all 7 stages immediately. Start with:
- Requirements → Code → System Test

Then add others as you get comfortable.

### 2. **Use Feature Flags**
Every task should have a feature flag:
```yaml
feature-task-5-payment-processing: false  # Default off
```

### 3. **Keep Intents Focused**
One intent = one user story or small feature
Better to have INT-001, INT-002, INT-003 than one huge INT-001

### 4. **Tag Everything with REQ Keys**
In code:
```javascript
// Implements: REQ-F-AUTH-001
function login(email, password) { ... }
```

In tests:
```javascript
// Validates: REQ-F-AUTH-001
test('user can login with valid credentials', ...)
```

In commits:
```
Implement user login (REQ-F-AUTH-001)
```

### 5. **Use Check-ins**
During `/start-session`, set check-in frequency (15-30 min).
Update `.ai-workspace/session/current_session.md` regularly.

---

## Troubleshooting

### Issue: Commands not working

```bash
# Check if commands installed
ls .claude/commands/

# Reinstall if needed
python /Users/jim/src/apps/ai_sdlc_method/installers/setup_commands.py --force
```

### Issue: Plugins not loading

```bash
# Check global plugins
ls ~/.config/claude/plugins/

# Reinstall if needed
cd /Users/jim/src/apps/ai_sdlc_method
python installers/setup_plugins.py --global --bundle startup --force
```

### Issue: Configuration not found

```bash
# Check config file exists
cat config/config.yml

# Verify plugin paths
ls ~/.config/claude/plugins/aisdlc-methodology/config/stages_config.yml
```

---

## Quick Reference Card

### One-Time Global Setup
```bash
cd /Users/jim/src/apps/ai_sdlc_method
python installers/setup_plugins.py --global --bundle startup
```

### For Each New Project
```bash
# 1. Create project
mkdir my-new-project && cd my-new-project
git init

# 2. Install tools
python /Users/jim/src/apps/ai_sdlc_method/installers/setup_all.py

# 3. Create intent and config
touch INTENT.md
mkdir config && touch config/config.yml

# 4. Start coding
/start-session
```

---

## Next Steps

1. **Read the guide**: `cat .ai-workspace/README.md`
2. **Review the example**: `/Users/jim/src/apps/ai_sdlc_method/examples/local_projects/customer_portal/`
3. **Start your first session**: `/start-session`
4. **Generate requirements**: Ask Claude to process your INTENT.md

---

## Getting Help

- **Workspace Guide**: `.ai-workspace/README.md`
- **Example Project**: `/Users/jim/src/apps/ai_sdlc_method/examples/local_projects/customer_portal/`
- **Complete Docs**: `/Users/jim/src/apps/ai_sdlc_method/docs/`
- **Plugin Docs**: `~/.config/claude/plugins/aisdlc-methodology/README.md`

---

**"Excellence or nothing"** 🔥

Ready to build great software with AI-assisted development!
