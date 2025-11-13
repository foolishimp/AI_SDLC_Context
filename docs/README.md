# AI_SDLC_Context Documentation

Complete documentation for the **AI-Augmented Software Development Lifecycle (AI SDLC)** framework.

---

## 🎯 Start Here

### ⭐ Core Methodology Document

**[ai_sdlc_guide.md](ai_sdlc_guide.md)** - The complete 7-stage AI SDLC methodology (3,300+ lines)

**Sections**:
- 1.0 Introduction - What is AI SDLC?
- 2.0 End-to-End Intent Lifecycle
- 3.0 Builder Pipeline Overview
- **4.0 Requirements Stage** - Intent → Structured requirements
- **5.0 Design Stage** - Requirements → Technical solution
- **6.0 Tasks Stage** - Work breakdown + Jira orchestration
- **7.0 Code Stage** - TDD implementation (RED→GREEN→REFACTOR)
- **8.0 System Test Stage** - BDD integration testing
- **9.0 UAT Stage** - Business validation
- **10.0 Runtime Feedback Stage** - Production telemetry feedback
- 11.0 Personas & Collaboration
- 12.0 Data Quality Integration
- 13.0 Governance & Compliance

👉 **Read this first** to understand the complete methodology!

---

## 📚 Quick Start

**New to AI_SDLC_Context?** Start here:

1. **[../README.md](../README.md)** - Project overview and quick start
2. **[ai_sdlc_guide.md](ai_sdlc_guide.md)** - Complete 7-stage methodology
3. **[../examples/local_projects/customer_portal/](../examples/local_projects/customer_portal/)** - Example project walkthrough
4. **[../plugins/aisdlc-methodology/README.md](../plugins/aisdlc-methodology/README.md)** - Methodology plugin documentation

---

## 📖 Core Documentation

### AI SDLC Methodology

- **[ai_sdlc_guide.md](ai_sdlc_guide.md)** ⭐ - Complete 7-stage methodology document
- **[ai_sdlc_full_flow.md](ai_sdlc_full_flow.md)** - Full flow diagrams and visualizations

### Plugin Documentation

- **[../plugins/aisdlc-methodology/README.md](../plugins/aisdlc-methodology/README.md)** - 7-stage methodology plugin
- **[../plugins/README.md](../plugins/README.md)** - Plugin creation and usage guide

### Example Projects

- **[../examples/local_projects/customer_portal/README.md](../examples/local_projects/customer_portal/README.md)** - Complete 7-stage workflow example
- **[../examples/README.md](../examples/README.md)** - All examples overview

---

## 🎓 Learning Path

### For Business Analysts / Product Owners

**Focus**: Requirements stage and business validation

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 4.0 (Requirements Stage)
2. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 9.0 (UAT Stage)
3. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Requirements artifacts
4. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Requirements agent configuration

**Key Concepts**: Intent transformation, requirement keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*), acceptance criteria, traceability

### For Architects / Technical Leads

**Focus**: Design stage and technical solution

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 5.0 (Design Stage)
2. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 11.0 (Personas & Collaboration)
3. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Design artifacts
4. Review [plugins/aisdlc-methodology/config/stages_config.yml](../plugins/aisdlc-methodology/config/stages_config.yml) - Design agent spec

**Key Concepts**: Requirements → Technical solution, component design, data models, API specifications, ADRs, traceability matrix

### For Developers

**Focus**: Code stage (TDD workflow)

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 7.0 (Code Stage)
2. Read [../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md](../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md) - Sacred Seven principles
3. Read [../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md) - TDD cycle
4. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Code stage walkthrough

**Key Concepts**: TDD (RED→GREEN→REFACTOR), requirement tagging, test coverage (≥80%), Sacred Seven principles

### For QA Engineers

**Focus**: System Test and UAT stages (BDD testing)

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 8.0 (System Test Stage)
2. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 9.0 (UAT Stage)
3. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - BDD testing examples
4. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Test agent configurations

**Key Concepts**: BDD (Given/When/Then), requirement coverage (≥95%), scenario-to-requirement matrix, business validation

### For DevOps / SRE

**Focus**: Runtime Feedback stage (observability)

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 10.0 (Runtime Feedback Stage)
2. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 2.0 (End-to-End Intent Lifecycle)
3. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Runtime feedback section
4. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Runtime feedback agent config

**Key Concepts**: Release manifests, requirement key tagging in telemetry, alerts → intents feedback loop, observability platforms

### For Project Managers / Scrum Masters

**Focus**: Tasks stage (work breakdown and orchestration)

1. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 6.0 (Tasks Stage)
2. Read [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 3.0 (Builder Pipeline Overview)
3. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Tasks stage
4. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Tasks orchestrator config

**Key Concepts**: Design → Work units, Jira integration, requirement key tagging, dependency tracking, agent orchestration

---

## 📘 Detailed Stage Documentation

### Stage 1: Requirements (Section 4.0)

**Agent**: Requirements Agent
**Input**: Raw intent from Intent Manager
**Output**: Structured requirements with unique keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*, REQ-BR-*)

**Documentation**:
- [ai_sdlc_guide.md - Section 4.0](ai_sdlc_guide.md)
- [stages_config.yml - requirements_stage](../plugins/aisdlc-methodology/config/stages_config.yml)
- [customer_portal - Requirements Config](../examples/local_projects/customer_portal/config/config.yml)

### Stage 2: Design (Section 5.0)

**Agent**: Design Agent / Solution Designer
**Input**: Structured requirements
**Output**: Component diagrams, data models, API specs, ADRs, traceability matrix

**Documentation**:
- [ai_sdlc_guide.md - Section 5.0](ai_sdlc_guide.md)
- [stages_config.yml - design_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 3: Tasks (Section 6.0)

**Agent**: Tasks Stage Orchestrator
**Input**: Design artifacts
**Output**: Jira tickets with requirement tags, dependency graph, capacity planning

**Documentation**:
- [ai_sdlc_guide.md - Section 6.0](ai_sdlc_guide.md)
- [stages_config.yml - tasks_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 4: Code (Section 7.0)

**Agent**: Code Agent / Developer Agent
**Input**: Work units from Tasks stage
**Output**: Production code with requirement tags, unit tests, integration tests

**Methodology**: TDD (RED → GREEN → REFACTOR) + Sacred Seven principles

**Documentation**:
- [ai_sdlc_guide.md - Section 7.0](ai_sdlc_guide.md)
- [stages_config.yml - code_stage](../plugins/aisdlc-methodology/config/stages_config.yml)
- [Sacred Seven Principles](../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md)
- [TDD Workflow](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)

### Stage 5: System Test (Section 8.0)

**Agent**: System Test Agent / QA Agent
**Input**: Deployed code
**Output**: BDD feature files (Gherkin), step definitions, coverage matrix

**Methodology**: BDD (Given/When/Then)

**Documentation**:
- [ai_sdlc_guide.md - Section 8.0](ai_sdlc_guide.md)
- [stages_config.yml - system_test_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 6: UAT (Section 9.0)

**Agent**: UAT Agent
**Input**: System test passed
**Output**: Manual UAT test cases, automated UAT tests, business sign-off

**Methodology**: BDD in pure business language

**Documentation**:
- [ai_sdlc_guide.md - Section 9.0](ai_sdlc_guide.md)
- [stages_config.yml - uat_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 7: Runtime Feedback (Section 10.0)

**Agent**: Runtime Feedback Agent
**Input**: Production deployment
**Output**: Release manifests, runtime telemetry (tagged with REQ keys), alerts, new intents

**Documentation**:
- [ai_sdlc_guide.md - Section 10.0](ai_sdlc_guide.md)
- [stages_config.yml - runtime_feedback_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

---

## 🔗 Related Documentation

### MCP Service (For Non-Claude LLMs)

- **[../mcp_service/README.md](../mcp_service/README.md)** - MCP service overview
- **[../mcp_service/MCP_SDLC_INTEGRATION_PLAN.md](../mcp_service/MCP_SDLC_INTEGRATION_PLAN.md)** - 7-stage integration plan
- **[../mcp_service/docs/PERSONAS.md](../mcp_service/docs/PERSONAS.md)** - Persona-based context management

### Configuration System (Legacy)

These documents describe the underlying configuration merging system:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture (config merging)
- **[guides/MERGE_KEYS_EXPLAINED.md](guides/MERGE_KEYS_EXPLAINED.md)** - How configuration merging works
- **[guides/CREATING_MERGE_TUPLES.md](guides/CREATING_MERGE_TUPLES.md)** - Static tuple composition
- **[guides/DYNAMIC_MERGE_TUPLES.md](guides/DYNAMIC_MERGE_TUPLES.md)** - Runtime tuple composition

**Note**: Most users don't need these - the Claude Code plugin system handles merging automatically.

---

## 🗺️ Documentation Map

### By Topic

#### **AI SDLC Methodology** (Start Here!)
- [ai_sdlc_guide.md](ai_sdlc_guide.md) - Complete methodology
- [ai_sdlc_full_flow.md](ai_sdlc_full_flow.md) - Flow diagrams
- [../plugins/aisdlc-methodology/](../plugins/aisdlc-methodology/) - Plugin implementation

#### **Examples & Walkthroughs**
- [../examples/local_projects/customer_portal/](../examples/local_projects/customer_portal/) - Complete 7-stage example
- [../examples/local_projects/api_platform/](../examples/local_projects/api_platform/) - Public API example
- [../examples/README.md](../examples/README.md) - All examples

#### **Principles & Processes**
- [../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md](../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md) - Sacred Seven
- [../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md) - TDD workflow
- [../plugins/aisdlc-methodology/docs/guides/](../plugins/aisdlc-methodology/docs/guides/) - Practical guides

#### **Plugin System**
- [../plugins/README.md](../plugins/README.md) - Plugin creation guide
- [../plugins/aisdlc-methodology/README.md](../plugins/aisdlc-methodology/README.md) - Methodology plugin
- [../README.md](../README.md) - Marketplace setup

#### **MCP Service**
- [../mcp_service/README.md](../mcp_service/README.md) - MCP overview
- [../mcp_service/MCP_SDLC_INTEGRATION_PLAN.md](../mcp_service/MCP_SDLC_INTEGRATION_PLAN.md) - Integration plan
- [../mcp_service/docs/](../mcp_service/docs/) - MCP documentation

---

## 🔍 Common Questions

**"What is the AI SDLC methodology?"**
→ [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 1.0 (Introduction)

**"How do the 7 stages work?"**
→ [ai_sdlc_guide.md](ai_sdlc_guide.md) - Sections 4.0-10.0

**"How does requirement traceability work?"**
→ [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 4.3.4 (Requirement Keys)
→ [customer_portal example](../examples/local_projects/customer_portal/README.md) - Traceability section

**"What are the Sacred Seven principles?"**
→ [../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md](../plugins/aisdlc-methodology/docs/principles/SACRED_SEVEN.md)

**"How does TDD work in this methodology?"**
→ [ai_sdlc_guide.md](ai_sdlc_guide.md) - Section 7.0 (Code Stage)
→ [../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)

**"How does BDD testing work?"**
→ [ai_sdlc_guide.md](ai_sdlc_guide.md) - Sections 8.0 & 9.0 (System Test & UAT)

**"How do I install and use the plugin?"**
→ [../README.md](../README.md) - Quick Start section

**"How do I create my own project with this methodology?"**
→ [../plugins/README.md](../plugins/README.md) - Plugin creation guide
→ [customer_portal example](../examples/local_projects/customer_portal/README.md)

**"Can I use this with non-Claude LLMs?"**
→ [../mcp_service/README.md](../mcp_service/README.md)

---

## 📦 Documentation Structure

```
docs/
├── README.md                           # This file
├── ai_sdlc_guide.md                   # ⭐ Complete 7-stage methodology (3,300+ lines)
├── ai_sdlc_full_flow.md               # Flow diagrams
│
├── ARCHITECTURE.md                     # Config system architecture (legacy)
├── MCP_SETUP.md                        # MCP server setup (legacy)
├── USAGE_EXAMPLES.md                   # Usage examples (legacy)
├── SUBAGENTS_GUIDE.md                  # Subagents guide (legacy)
│
├── guides/                             # Configuration system guides (legacy)
│   ├── CREATING_MERGE_TUPLES.md
│   ├── DYNAMIC_MERGE_TUPLES.md
│   ├── MERGE_KEYS_EXPLAINED.md
│   └── URI_REPLACEMENT_GUIDE.md
│
├── quick-reference/                    # Config quick references (legacy)
│   ├── MERGE_KEYS_SUMMARY.md
│   ├── MERGE_TUPLE_QUICK_REFERENCE.md
│   ├── DYNAMIC_TUPLES_QUICK_REF.md
│   └── URI_REPLACEMENT_SUMMARY.md
│
├── design/                             # Design documentation (historical)
│   ├── DESIGN_REVIEW_SUMMARY.md
│   ├── METHODOLOGY_PROJECT_DESIGN_REVIEW.md
│   └── FULL_CONTEXT_STATE_FEATURE.md
│
└── deprecated/                         # Archived documentation
    ├── AI_INIT_REVIEW.md
    ├── RENAME_SUMMARY.md
    ├── STATUS.md
    └── EXAMPLE_WALKTHROUGH.md
```

---

## 🤝 Contributing

When adding new documentation:

1. **AI SDLC methodology docs** → Update [ai_sdlc_guide.md](ai_sdlc_guide.md) or add to [../plugins/aisdlc-methodology/docs/](../plugins/aisdlc-methodology/docs/)
2. **Examples** → Add to [../examples/](../examples/)
3. **Plugin docs** → Add to [../plugins/](../plugins/)
4. **MCP service docs** → Add to [../mcp_service/docs/](../mcp_service/docs/)
5. **Update this README** → Add links to new documentation

---

## 📄 License

See [../LICENSE](../LICENSE) for license information.

---

*Last updated: 2025-11-14*

**"Excellence or nothing"** 🔥
