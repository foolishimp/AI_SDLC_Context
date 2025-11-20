# MCP Service Integration with 7-Stage AI SDLC Methodology

**Date**: 2025-11-14
**Plugin**: aisdlc-methodology v2.0.0
**Reference**: `/docs/ai_sdlc_method.md` (Sections 4.0-10.0)

---

## Executive Summary

The MCP service currently supports:
- ✅ Project CRUD operations
- ✅ Configuration merging
- ✅ Persona-based views (human roles: BA, Engineer, QA, etc.)
- ✅ Git-backed storage

**What Needs Updating**:
- 🔄 Integrate 7-stage AI SDLC agent configurations
- 🔄 Align personas with AI agent roles
- 🔄 Support requirement key traceability
- 🔄 Enable stage-specific context loading
- 🔄 Add orchestration tools for agent workflows

---

## Current State vs Target State

### Current State (Legacy)

```
MCP Service
├── Project CRUD (✅ Works)
├── Content Management (✅ Works)
├── Personas (Human Roles)
│   ├── Business Analyst
│   ├── Software Engineer
│   ├── QA Engineer
│   ├── DevOps Engineer
│   └── Security Engineer
└── Merge Engine (✅ Works)
```

**Limitation**: Personas are human-centric, not aligned with AI SDLC stages

---

### Target State (7-Stage Integration)

```
MCP Service
├── Project CRUD (✅ Exists)
├── Content Management (✅ Exists)
├── AI SDLC Agents (NEW)
│   ├── Requirements Agent (Section 4.0)
│   ├── Design Agent (Section 5.0)
│   ├── Tasks Orchestrator (Section 6.0)
│   ├── Code Agent (Section 7.0)
│   ├── System Test Agent (Section 8.0)
│   ├── UAT Agent (Section 9.0)
│   └── Runtime Feedback Agent (Section 10.0)
├── Human Personas (✅ Exists, but enhanced)
│   ├── Product Owner (works with Requirements Agent)
│   ├── Architect (works with Design Agent)
│   ├── Developer (works with Code Agent)
│   └── QA Lead (works with System Test/UAT Agents)
├── Stage Context Loading (NEW)
├── Requirement Traceability (NEW)
└── Agent Orchestration Tools (NEW)
```

**Enhancement**: Dual-level support for both AI agents AND human roles

---

## Integration Strategy

### 1. AI Agent Personas (NEW)

Create agent persona configurations for each SDLC stage:

```
mcp_service/
├── server/
│   └── agent_personas/          # NEW directory
│       ├── requirements_agent.yml
│       ├── design_agent.yml
│       ├── tasks_orchestrator.yml
│       ├── code_agent.yml
│       ├── system_test_agent.yml
│       ├── uat_agent.yml
│       └── runtime_feedback_agent.yml
```

#### Example: Requirements Agent Persona

```yaml
# agent_personas/requirements_agent.yml
agent:
  name: "Requirements Agent"
  stage: "requirements"
  section_ref: "4.0"

  role: "Intent Store & Traceability Hub"

  purpose: |
    Transform raw intent into structured requirements with unique,
    immutable keys that flow through the entire SDLC.

  responsibilities:
    - "Parse raw intent from Intent Manager"
    - "Generate requirement artifacts (user stories, NFRs, data requirements)"
    - "Assign unique requirement keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*)"
    - "Process feedback from all downstream stages"
    - "Maintain bi-directional traceability"

  inputs:
    - type: "intent"
      source: "Intent Manager"
      format: "natural language or structured"
    - type: "feedback"
      sources: ["design", "tasks", "code", "system_test", "uat", "runtime_feedback"]

  outputs:
    - type: "functional_requirements"
      prefix: "REQ-F"
      template: "file://templates/user_story.md"
    - type: "non_functional_requirements"
      prefix: "REQ-NFR"
      template: "file://templates/nfr.md"
    - type: "data_requirements"
      prefix: "REQ-DATA"
      template: "file://templates/data_requirement.md"
    - type: "business_rules"
      prefix: "REQ-BR"
      template: "file://templates/business_rule.md"

  quality_gates:
    - "All requirements have unique keys"
    - "All requirements have acceptance criteria"
    - "Product Owner review complete"
    - "Business Analyst review complete"
    - "Data Steward review complete (for REQ-DATA-*)"

  context:
    standards:
      - "file://../../plugins/aisdlc-methodology/config/stages_config.yml#requirements_stage"
    templates:
      - "file://templates/requirements/*"
    constraints:
      - "Requirement keys must be immutable"
      - "All requirements must have traceability to intent"

  collaborates_with:
    human_personas:
      - "Product Owner" (approval authority)
      - "Business Analyst" (requirement elaboration)
      - "Data Steward" (data requirements)
    ai_agents:
      - "Design Agent" (receives requirements)
      - "All stages" (receives feedback)

  traceability:
    requirement_key_format: "REQ-{TYPE}-{CATEGORY}-{ID:03d}"
    immutable_keys: true
    bidirectional_tracking: true
    feedback_loop: true
```

---

### 2. Enhanced Human Personas

Update human personas to work **with** AI agents:

```yaml
# personas/product_owner.yml (ENHANCED)
persona:
  name: "Product Owner"
  role: "product_owner"

  # NEW: Link to AI agent they work with
  primary_agent: "requirements_agent"
  stage: "requirements"

  focus_areas:
    - "Business value prioritization"
    - "Requirement approval"
    - "Acceptance criteria validation"
    - "UAT sign-off"

  agent_collaboration:
    requirements_agent:
      authority: "approval"
      reviews: ["all requirements", "acceptance criteria"]
    uat_agent:
      authority: "sign-off"
      participates_in: ["UAT test case creation", "business validation"]

  # Existing persona config...
  preferences:
    documentation:
      style: "narrative"
      detail_level: "business_focused"

  overrides:
    # Focus on requirements artifacts
    ai_sdlc:
      stages:
        requirements:
          emphasize:
            - "Business value"
            - "Acceptance criteria"
            - "User stories"
```

---

### 3. Stage Context Loading (NEW)

Add MCP tools to load stage-specific context:

#### New MCP Tools

```python
# server/stage_tools.py (NEW FILE)

@server.call_tool()
async def load_stage_context(
    project_name: str,
    stage: str,  # requirements, design, tasks, code, system_test, uat, runtime_feedback
    agent_mode: bool = True  # True for AI agent, False for human persona
):
    """
    Load stage-specific context from project configuration.

    Args:
        project_name: Project to load context from
        stage: SDLC stage name
        agent_mode: Load as AI agent (True) or human (False)

    Returns:
        Stage-specific configuration with agent specs or human view
    """
    # Load project
    project = project_repo.load_project(project_name)

    # Load stage config from aisdlc-methodology plugin
    stage_config = load_stage_config(stage)

    if agent_mode:
        # Load AI agent persona
        agent_persona = load_agent_persona(f"{stage}_agent")

        return {
            "project": project_name,
            "stage": stage,
            "mode": "ai_agent",
            "agent": agent_persona,
            "config": merge_project_with_stage(project, stage_config)
        }
    else:
        # Load human persona for this stage
        human_persona = get_human_persona_for_stage(stage)

        return {
            "project": project_name,
            "stage": stage,
            "mode": "human",
            "persona": human_persona,
            "config": merge_project_with_stage(project, stage_config)
        }


@server.call_tool()
async def list_available_stages():
    """List all 7 SDLC stages with their agents."""
    return [
        {
            "stage": "requirements",
            "section": "4.0",
            "agent": "Requirements Agent",
            "purpose": "Intent to structured requirements with unique keys"
        },
        {
            "stage": "design",
            "section": "5.0",
            "agent": "Design Agent / Solution Designer",
            "purpose": "Requirements to implementable technical and data solution"
        },
        {
            "stage": "tasks",
            "section": "6.0",
            "agent": "Tasks Stage Orchestrator",
            "purpose": "Work breakdown with Jira integration and agent orchestration"
        },
        {
            "stage": "code",
            "section": "7.0",
            "agent": "Code Agent / Developer Agent",
            "purpose": "TDD-driven implementation (RED → GREEN → REFACTOR)"
        },
        {
            "stage": "system_test",
            "section": "8.0",
            "agent": "System Test Agent / QA Agent",
            "purpose": "BDD integration testing (Given/When/Then)"
        },
        {
            "stage": "uat",
            "section": "9.0",
            "agent": "UAT Agent",
            "purpose": "Business validation with BDD in pure business language"
        },
        {
            "stage": "runtime_feedback",
            "section": "10.0",
            "agent": "Runtime Feedback Agent",
            "purpose": "Production telemetry and feedback loop closure"
        }
    ]


@server.call_tool()
async def trace_requirement_key(
    requirement_key: str,  # e.g., "REQ-F-AUTH-001"
    project_name: str
):
    """
    Trace a requirement key through all SDLC stages.

    Args:
        requirement_key: Requirement identifier (e.g., REQ-F-AUTH-001)
        project_name: Project containing the requirement

    Returns:
        Traceability chain showing where requirement appears in each stage
    """
    # Load project
    project = project_repo.load_project(project_name)

    # Trace through stages
    trace = {
        "requirement_key": requirement_key,
        "stages": {}
    }

    # Requirements stage
    trace["stages"]["requirements"] = find_requirement_in_requirements(
        project, requirement_key
    )

    # Design stage
    trace["stages"]["design"] = find_requirement_in_design(
        project, requirement_key
    )

    # Tasks stage (Jira tickets)
    trace["stages"]["tasks"] = find_requirement_in_tasks(
        project, requirement_key
    )

    # Code stage
    trace["stages"]["code"] = find_requirement_in_code(
        project, requirement_key
    )

    # Test stages
    trace["stages"]["system_test"] = find_requirement_in_tests(
        project, requirement_key, test_type="system"
    )

    trace["stages"]["uat"] = find_requirement_in_tests(
        project, requirement_key, test_type="uat"
    )

    # Runtime feedback
    trace["stages"]["runtime"] = find_requirement_in_runtime(
        project, requirement_key
    )

    return trace


@server.call_tool()
async def get_stage_quality_gates(
    project_name: str,
    stage: str
):
    """Get quality gates for a specific stage."""
    # Load stage config
    stage_config = load_stage_config(stage)

    # Load project overrides
    project = project_repo.load_project(project_name)
    project_gates = project.get(f"ai_sdlc.stages.{stage}.quality_gates", [])

    # Merge project-specific with stage defaults
    return {
        "stage": stage,
        "project": project_name,
        "quality_gates": merge_quality_gates(
            stage_config["quality_gates"],
            project_gates
        )
    }
```

---

### 4. Requirement Traceability Support

#### New Data Structures

```python
# storage/traceability_tracker.py (NEW FILE)

class TraceabilityTracker:
    """Track requirement keys through SDLC stages."""

    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def record_requirement_usage(
        self,
        project_name: str,
        requirement_key: str,
        stage: str,
        artifact_path: str,
        artifact_type: str
    ):
        """
        Record that a requirement was used in a specific stage.

        Args:
            project_name: Project name
            requirement_key: Requirement ID (REQ-F-AUTH-001)
            stage: SDLC stage name
            artifact_path: Path to artifact using requirement
            artifact_type: Type (code, test, doc, jira_ticket, etc.)
        """
        # Store in project's traceability database
        trace_file = self.project_repo.get_project_path(project_name) / ".traceability.json"

        # Load existing traces
        traces = self._load_traces(trace_file)

        # Add new trace
        if requirement_key not in traces:
            traces[requirement_key] = {
                "requirement_key": requirement_key,
                "stages": {}
            }

        if stage not in traces[requirement_key]["stages"]:
            traces[requirement_key]["stages"][stage] = []

        traces[requirement_key]["stages"][stage].append({
            "artifact_path": artifact_path,
            "artifact_type": artifact_type,
            "recorded_at": datetime.now().isoformat()
        })

        # Save traces
        self._save_traces(trace_file, traces)

    def get_requirement_trace(
        self,
        project_name: str,
        requirement_key: str
    ) -> Dict[str, Any]:
        """Get full traceability chain for a requirement."""
        trace_file = self.project_repo.get_project_path(project_name) / ".traceability.json"
        traces = self._load_traces(trace_file)

        return traces.get(requirement_key, {
            "requirement_key": requirement_key,
            "stages": {},
            "warning": "No traceability data found"
        })
```

---

### 5. Agent Orchestration Tools (NEW)

```python
# server/agent_orchestration.py (NEW FILE)

@server.call_tool()
async def orchestrate_stage_workflow(
    project_name: str,
    stage: str,
    inputs: Dict[str, Any]
):
    """
    Orchestrate an AI agent workflow for a specific stage.

    Example:
        orchestrate_stage_workflow(
            project_name="customer_portal",
            stage="requirements",
            inputs={
                "intent": "Users need self-service portal",
                "stakeholder": "Product Owner"
            }
        )

    Returns:
        Stage outputs with requirement keys
    """
    # Load stage agent
    agent = load_agent_persona(f"{stage}_agent")

    # Load project context
    project = project_repo.load_project(project_name)
    stage_config = merge_project_with_stage(project, load_stage_config(stage))

    # Execute stage workflow
    result = await execute_agent_workflow(
        agent=agent,
        config=stage_config,
        inputs=inputs
    )

    # Record traceability
    if "requirement_keys" in result:
        for req_key in result["requirement_keys"]:
            traceability_tracker.record_requirement_usage(
                project_name=project_name,
                requirement_key=req_key,
                stage=stage,
                artifact_path=result.get("artifact_path", ""),
                artifact_type=result.get("artifact_type", "")
            )

    return result
```

---

## Implementation Checklist

### Phase 1: Agent Personas (Week 1)
- [ ] Create `server/agent_personas/` directory
- [ ] Implement 7 agent persona YAML files (one per stage)
- [ ] Update `PersonaManager` to support agent personas
- [ ] Add `load_agent_persona()` function

### Phase 2: Enhanced Human Personas (Week 1)
- [ ] Update existing personas (BA, Engineer, QA, etc.)
- [ ] Add `primary_agent` and `stage` fields
- [ ] Add `agent_collaboration` section
- [ ] Document which humans work with which agents

### Phase 3: Stage Context Loading (Week 2)
- [ ] Create `server/stage_tools.py`
- [ ] Implement `load_stage_context()` MCP tool
- [ ] Implement `list_available_stages()` MCP tool
- [ ] Implement `get_stage_quality_gates()` MCP tool
- [ ] Add tests

### Phase 4: Traceability Support (Week 2)
- [ ] Create `storage/traceability_tracker.py`
- [ ] Implement `TraceabilityTracker` class
- [ ] Implement `trace_requirement_key()` MCP tool
- [ ] Add `.traceability.json` to project storage format
- [ ] Add tests

### Phase 5: Agent Orchestration (Week 3)
- [ ] Create `server/agent_orchestration.py`
- [ ] Implement `orchestrate_stage_workflow()` MCP tool
- [ ] Implement `execute_agent_workflow()` helper
- [ ] Add workflow state management
- [ ] Add tests

### Phase 6: Documentation Updates (Week 3)
- [ ] Update `README.md` with 7-stage overview
- [ ] Update `docs/PERSONAS.md` with AI agents
- [ ] Update `docs/API.md` with new MCP tools
- [ ] Create `docs/AI_AGENTS.md` guide
- [ ] Update examples to demonstrate 7-stage workflow

### Phase 7: Examples (Week 4)
- [ ] Create `examples/seven_stage_workflow.py`
- [ ] Create `examples/requirement_traceability.py`
- [ ] Create `examples/agent_orchestration.py`
- [ ] Update `examples/persona_demo.py` to include agents
- [ ] Create example project with full 7-stage config

---

## Benefits of This Integration

### For AI Agents
✅ **Clear Role Definition**: Each agent knows its responsibilities
✅ **Context Loading**: Load stage-specific configuration easily
✅ **Traceability**: Track requirements through entire lifecycle
✅ **Orchestration**: Coordinate multi-stage workflows

### For Human Users
✅ **Dual-Level Personas**: Work as human OR instruct AI agent
✅ **Stage Visibility**: See what each SDLC stage requires
✅ **Quality Gates**: Understand pass/fail criteria per stage
✅ **Requirement Tracking**: Trace any requirement end-to-end

### For Organizations
✅ **Compliance**: Full audit trail through SDLC
✅ **Standardization**: Consistent process across projects
✅ **Automation**: AI agents automate SDLC stages
✅ **Traceability**: Bidirectional requirement tracking

---

## Example Usage After Integration

### Load AI Agent Context

```python
# Via MCP client (Claude)
"Load customer_portal project with requirements agent context"

# Result: Claude receives:
# - Requirements Agent persona
# - Customer portal project config
# - Requirement templates
# - Quality gates for requirements stage
# - Traceability tools

# Claude can now act as Requirements Agent!
```

### Trace Requirement

```python
# Via MCP client
"Trace requirement REQ-F-AUTH-001 through all stages in customer_portal"

# Result:
# {
#   "requirement_key": "REQ-F-AUTH-001",
#   "stages": {
#     "requirements": {...},
#     "design": {...},
#     "tasks": {...},
#     "code": {...},
#     "system_test": {...},
#     "uat": {...},
#     "runtime": {...}
#   }
# }
```

### Orchestrate Workflow

```python
# Via MCP client
"Start requirements stage workflow for customer_portal with intent:
'Users need self-service portal'"

# Result: Requirements Agent processes intent and generates:
# - REQ-F-AUTH-001: User authentication
# - REQ-F-TICKET-001: Support ticket creation
# - REQ-F-ORDER-001: Order tracking
# [All with full traceability]
```

---

## Backward Compatibility

✅ **Existing functionality preserved**:
- Project CRUD still works
- Content management still works
- Human personas still work
- Merge operations still work

✅ **New features are additive**:
- Agent personas are new, don't break existing personas
- Stage tools are new MCP tools
- Traceability is opt-in

✅ **Migration path**:
- Existing projects work without changes
- New projects can opt into 7-stage methodology
- Human personas can be gradually enhanced

---

## Conclusion

This integration plan brings the MCP service into full alignment with the 7-stage AI SDLC methodology while maintaining backward compatibility. The phased approach allows incremental implementation over 4 weeks.

**Next Steps**:
1. Review and approve this plan
2. Begin Phase 1: Agent Personas
3. Update documentation as we go
4. Create examples for each phase

**Reference**:
- Plugin: `/plugins/aisdlc-methodology` v2.0.0
- Overview: `/docs/ai_sdlc_overview.md`
- Method: `/docs/ai_sdlc_method.md`
- Example: `/examples/local_projects/customer_portal/`
