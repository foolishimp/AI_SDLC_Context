# ai_sdlc_method Documentation

Complete documentation for the **AI-Augmented Software Development Lifecycle (AI SDLC)** framework.

---

## 🎯 Start Here

### ⭐ Core Methodology Documents

**Three-tier documentation structure:**

1. **[ai_sdlc_overview.md](ai_sdlc_overview.md)** - High-level introduction (~30 min read)
   - Quick overview of AI SDLC concepts
   - Perfect for executives and stakeholders
   - Visual diagrams and examples

2. **[ai_sdlc_method.md](ai_sdlc_method.md)** ⭐ - Complete methodology reference (3,300+ lines)
   - Section 1.0: Introduction - What is AI SDLC?
   - Section 2.0: End-to-End Intent Lifecycle
   - Section 3.0: Builder Pipeline Overview
   - **Section 4.0: Requirements Stage** - Intent → Structured requirements
   - **Section 5.0: Design Stage** - Requirements → Technical solution
   - **Section 6.0: Tasks Stage** - Work breakdown + Jira orchestration
   - **Section 7.0: Code Stage** - TDD implementation (RED→GREEN→REFACTOR)
   - **Section 8.0: System Test Stage** - BDD integration testing
   - **Section 9.0: UAT Stage** - Business validation
   - **Section 10.0: Runtime Feedback Stage** - Production telemetry feedback
   - Section 11.0: Personas & Collaboration
   - Section 12.0: Data Quality Integration
   - Section 13.0: Governance & Compliance

3. **[ai_sdlc_appendices.md](ai_sdlc_appendices.md)** - Technical deep-dives
   - Category theory foundations
   - Ecosystem requirements integration
   - Advanced technical concepts

👉 **Quick start**: Read [ai_sdlc_overview.md](ai_sdlc_overview.md) first, then dive into [ai_sdlc_method.md](ai_sdlc_method.md) for details!

---

## 📚 Quick Start

**New to ai_sdlc_method?** Start here:

1. **[../README.md](../README.md)** - Project overview and quick start
2. **[ai_sdlc_overview.md](ai_sdlc_overview.md)** - High-level overview (30 min read)
3. **[ai_sdlc_method.md](ai_sdlc_method.md)** - Complete 7-stage methodology (detailed reference)
4. **[../examples/local_projects/customer_portal/](../examples/local_projects/customer_portal/)** - Example project walkthrough
5. **[../plugins/aisdlc-methodology/README.md](../plugins/aisdlc-methodology/README.md)** - Methodology plugin documentation

---

## 📖 Core Documentation

### AI SDLC Methodology

- **[ai_sdlc_overview.md](ai_sdlc_overview.md)** - High-level introduction (executives, stakeholders)
- **[ai_sdlc_method.md](ai_sdlc_method.md)** ⭐ - Complete 7-stage methodology (practitioners)
- **[ai_sdlc_appendices.md](ai_sdlc_appendices.md)** - Technical deep-dives (advanced topics)
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

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 4.0 (Requirements Stage)
3. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 9.0 (UAT Stage)
4. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Requirements artifacts
5. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Requirements agent configuration

**Key Concepts**: Intent transformation, requirement keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*), acceptance criteria, traceability

### For Architects / Technical Leads

**Focus**: Design stage and technical solution

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 5.0 (Design Stage)
3. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 11.0 (Personas & Collaboration)
4. Read [ai_sdlc_appendices.md](ai_sdlc_appendices.md) - Advanced architectural concepts
5. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Design artifacts
6. Review [plugins/aisdlc-methodology/config/stages_config.yml](../plugins/aisdlc-methodology/config/stages_config.yml) - Design agent spec

**Key Concepts**: Requirements → Technical solution, component design, data models, API specifications, ADRs, traceability matrix

### For Developers

**Focus**: Code stage (TDD workflow)

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 7.0 (Code Stage)
3. Read [../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md](../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md) - Key Principles
4. Read [../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md) - TDD cycle
5. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Code stage walkthrough

**Key Concepts**: TDD (RED→GREEN→REFACTOR), requirement tagging, test coverage (≥80%), Key Principles

### For QA Engineers

**Focus**: System Test and UAT stages (BDD testing)

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 8.0 (System Test Stage)
3. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 9.0 (UAT Stage)
4. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - BDD testing examples
5. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Test agent configurations

**Key Concepts**: BDD (Given/When/Then), requirement coverage (≥95%), scenario-to-requirement matrix, business validation

### For DevOps / SRE

**Focus**: Runtime Feedback stage (observability)

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 10.0 (Runtime Feedback Stage)
3. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 2.0 (End-to-End Intent Lifecycle)
4. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Runtime feedback section
5. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Runtime feedback agent config

**Key Concepts**: Release manifests, requirement key tagging in telemetry, alerts → intents feedback loop, observability platforms

### For Project Managers / Scrum Masters

**Focus**: Tasks stage (work breakdown and orchestration)

1. Read [ai_sdlc_overview.md](ai_sdlc_overview.md) - Get the big picture
2. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 6.0 (Tasks Stage)
3. Read [ai_sdlc_method.md](ai_sdlc_method.md) - Section 3.0 (Builder Pipeline Overview)
4. Review [customer_portal example](../examples/local_projects/customer_portal/README.md) - Tasks stage
5. Review [customer_portal config](../examples/local_projects/customer_portal/config/config.yml) - Tasks orchestrator config

**Key Concepts**: Design → Work units, Jira integration, requirement key tagging, dependency tracking, agent orchestration

---

## 📘 Detailed Stage Documentation

### Stage 1: Requirements (Section 4.0)

**Agent**: Requirements Agent
**Input**: Raw intent from Intent Manager
**Output**: Structured requirements with unique keys (REQ-F-*, REQ-NFR-*, REQ-DATA-*, REQ-BR-*)

**Documentation**:
- [ai_sdlc_method.md - Section 4.0](ai_sdlc_method.md#40-requirements-stage)
- [stages_config.yml - requirements_stage](../plugins/aisdlc-methodology/config/stages_config.yml)
- [customer_portal - Requirements Config](../examples/local_projects/customer_portal/config/config.yml)

### Stage 2: Design (Section 5.0)

**Agent**: Design Agent / Solution Designer
**Input**: Structured requirements
**Output**: Component diagrams, data models, API specs, ADRs, traceability matrix

**Documentation**:
- [ai_sdlc_method.md - Section 5.0](ai_sdlc_method.md#50-design-stage)
- [stages_config.yml - design_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 3: Tasks (Section 6.0)

**Agent**: Tasks Stage Orchestrator
**Input**: Design artifacts
**Output**: Jira tickets with requirement tags, dependency graph, capacity planning

**Documentation**:
- [ai_sdlc_method.md - Section 6.0](ai_sdlc_method.md#60-tasks-stage)
- [stages_config.yml - tasks_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 4: Code (Section 7.0)

**Agent**: Code Agent / Developer Agent
**Input**: Work units from Tasks stage
**Output**: Production code with requirement tags, unit tests, integration tests

**Methodology**: TDD (RED → GREEN → REFACTOR) + Key Principles

**Documentation**:
- [ai_sdlc_method.md - Section 7.0](ai_sdlc_method.md#70-code-stage)
- [stages_config.yml - code_stage](../plugins/aisdlc-methodology/config/stages_config.yml)
- [Key Principles](../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md)
- [TDD Workflow](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)

### Stage 5: System Test (Section 8.0)

**Agent**: System Test Agent / QA Agent
**Input**: Deployed code
**Output**: BDD feature files (Gherkin), step definitions, coverage matrix

**Methodology**: BDD (Given/When/Then)

**Documentation**:
- [ai_sdlc_method.md - Section 8.0](ai_sdlc_method.md#80-system-test-stage)
- [stages_config.yml - system_test_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 6: UAT (Section 9.0)

**Agent**: UAT Agent
**Input**: System test passed
**Output**: Manual UAT test cases, automated UAT tests, business sign-off

**Methodology**: BDD in pure business language

**Documentation**:
- [ai_sdlc_method.md - Section 9.0](ai_sdlc_method.md#90-uat-stage)
- [stages_config.yml - uat_stage](../plugins/aisdlc-methodology/config/stages_config.yml)

### Stage 7: Runtime Feedback (Section 10.0)

**Agent**: Runtime Feedback Agent
**Input**: Production deployment
**Output**: Release manifests, runtime telemetry (tagged with REQ keys), alerts, new intents

**Documentation**:
- [ai_sdlc_method.md - Section 10.0](ai_sdlc_method.md#100-runtime-feedback-stage)
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
- [ai_sdlc_overview.md](ai_sdlc_overview.md) - High-level overview
- [ai_sdlc_method.md](ai_sdlc_method.md) - Complete methodology
- [ai_sdlc_appendices.md](ai_sdlc_appendices.md) - Technical deep-dives
- [ai_sdlc_full_flow.md](ai_sdlc_full_flow.md) - Flow diagrams
- [../plugins/aisdlc-methodology/](../plugins/aisdlc-methodology/) - Plugin implementation

#### **Examples & Walkthroughs**
- [../examples/local_projects/customer_portal/](../examples/local_projects/customer_portal/) - Complete 7-stage example
- [../examples/local_projects/api_platform/](../examples/local_projects/api_platform/) - Public API example
- [../examples/README.md](../examples/README.md) - All examples

#### **Principles & Processes**
- [../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md](../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md) - Key Principles
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
→ [ai_sdlc_overview.md](ai_sdlc_overview.md) - Quick introduction
→ [ai_sdlc_method.md](ai_sdlc_method.md) - Section 1.0 (Introduction)

**"How do the 7 stages work?"**
→ [ai_sdlc_overview.md](ai_sdlc_overview.md) - High-level overview
→ [ai_sdlc_method.md](ai_sdlc_method.md) - Sections 4.0-10.0 (detailed)

**"How does requirement traceability work?"**
→ [ai_sdlc_method.md](ai_sdlc_method.md) - Section 4.3.4 (Requirement Keys)
→ [customer_portal example](../examples/local_projects/customer_portal/README.md) - Traceability section

**"What are the Key Principles?"**
→ [../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md](../plugins/aisdlc-methodology/docs/principles/KEY_PRINCIPLES.md)

**"How does TDD work in this methodology?"**
→ [ai_sdlc_method.md](ai_sdlc_method.md) - Section 7.0 (Code Stage)
→ [../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md](../plugins/aisdlc-methodology/docs/processes/TDD_WORKFLOW.md)

**"How does BDD testing work?"**
→ [ai_sdlc_method.md](ai_sdlc_method.md) - Sections 8.0 & 9.0 (System Test & UAT)

**"How do I install and use the plugin?"**
→ [../README.md](../README.md) - Quick Start section

**"How do I create my own project with this methodology?"**
→ [../plugins/README.md](../plugins/README.md) - Plugin creation guide
→ [customer_portal example](../examples/local_projects/customer_portal/README.md)

**"Can I use this with non-Claude LLMs?"**
→ [../mcp_service/README.md](../mcp_service/README.md)

**"What are the advanced technical concepts?"**
→ [ai_sdlc_appendices.md](ai_sdlc_appendices.md) - Category theory, ecosystem integration

---

## 📦 Documentation Structure

```
docs/
├── README.md                           # This file - Documentation index
│
├── ai_sdlc_overview.md                # ⭐ High-level overview (~30 min read)
├── ai_sdlc_method.md                  # ⭐ Complete 7-stage methodology (3,300+ lines)
├── ai_sdlc_appendices.md              # ⭐ Technical deep-dives (category theory, ecosystem)
├── ai_sdlc_full_flow.md               # Flow diagrams and visualizations
│
├── guides/                             # Role-specific application guides
│   └── README.md                       # Guide index (coming soon)
│
└── deprecated/                         # Archived documentation
    ├── ai_sdlc_guide_V1_0.md          # v1.0 methodology (replaced by ai_sdlc_method.md)
    ├── ai_sdlc_guide_V1_0.pdf         # v1.0 PDF version
    ├── ai_sdlc_guide_v1_2.md          # v1.2 pre-split version
    ├── ai_sdlc_executive_summary.md   # v1.2 executive summary
    ├── ARCHITECTURE.md                 # Legacy config system architecture
    ├── MCP_SETUP.md                    # Legacy MCP server setup
    ├── USAGE_EXAMPLES.md               # Legacy usage examples
    ├── SUBAGENTS_GUIDE.md              # Legacy subagents guide
    ├── AI_INIT_REVIEW.md               # ai_init integration review
    ├── ECOSYSTEM_*.md                  # Ecosystem integration drafts
    ├── CATEGORY_THEORY_REVIEW.md       # Category theory draft
    ├── CONSOLIDATION_PLAN.md           # Documentation consolidation plan
    ├── design/                         # Historical design documentation
    ├── guides/                         # Legacy configuration guides
    └── quick-reference/                # Legacy quick references
```

**Current Active Documentation** (v1.2):
- [ai_sdlc_overview.md](ai_sdlc_overview.md) - Start here for quick understanding
- [ai_sdlc_method.md](ai_sdlc_method.md) - Complete methodology reference
- [ai_sdlc_appendices.md](ai_sdlc_appendices.md) - Advanced technical concepts

---

## 🤝 Contributing

When adding new documentation:

1. **AI SDLC methodology docs** → Update [ai_sdlc_method.md](ai_sdlc_method.md) or add to [../plugins/aisdlc-methodology/docs/](../plugins/aisdlc-methodology/docs/)
2. **Overview updates** → Update [ai_sdlc_overview.md](ai_sdlc_overview.md) for high-level changes
3. **Technical deep-dives** → Add to [ai_sdlc_appendices.md](ai_sdlc_appendices.md)
4. **Examples** → Add to [../examples/](../examples/)
5. **Plugin docs** → Add to [../plugins/](../plugins/)
6. **MCP service docs** → Add to [../mcp_service/docs/](../mcp_service/docs/)
7. **Update this README** → Add links to new documentation

**Documentation Versioning**:
- Major methodology changes → Increment version in [ai_sdlc_method.md](ai_sdlc_method.md) header
- Archive previous versions → Move to [deprecated/](deprecated/)
- Update "Last updated" date below

---

## 📄 License

See [../LICENSE](../LICENSE) for license information.

---

*Last updated: 2025-11-20*

**Version**: Documentation restructured to reflect v1.2 methodology split into:
- Overview (ai_sdlc_overview.md)
- Method (ai_sdlc_method.md)
- Appendices (ai_sdlc_appendices.md)

**"Excellence or nothing"** 🔥
