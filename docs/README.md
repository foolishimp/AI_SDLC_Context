# AI_SDLC_Context Documentation

Complete documentation for the AI_SDLC_Context system.

---

## 📚 Quick Start

**New to AI_SDLC_Context?** Start here:

1. **[../README.md](../README.md)** - Project overview and features
2. **[../QUICKSTART.md](../QUICKSTART.md)** - Get started in 5 minutes
3. **[../PLUGIN_GUIDE.md](../PLUGIN_GUIDE.md)** - Plugin installation and usage

---

## 📖 Core Documentation

### System Architecture
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design
- **[MCP_SETUP.md](MCP_SETUP.md)** - MCP server setup guide
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Practical usage examples
- **[SUBAGENTS_GUIDE.md](SUBAGENTS_GUIDE.md)** - Creating and using subagents

---

## 📘 Detailed Guides

Comprehensive guides for advanced features:

- **[guides/CREATING_MERGE_TUPLES.md](guides/CREATING_MERGE_TUPLES.md)**
  - How to create inheritance chains
  - Setting up base_projects
  - Static tuple composition

- **[guides/DYNAMIC_MERGE_TUPLES.md](guides/DYNAMIC_MERGE_TUPLES.md)**
  - Runtime tuple composition
  - Using runtime_overrides
  - CI/CD integration

- **[guides/MERGE_KEYS_EXPLAINED.md](guides/MERGE_KEYS_EXPLAINED.md)**
  - How merge keys work
  - Dot-notation paths
  - Merge algorithm details

- **[guides/URI_REPLACEMENT_GUIDE.md](guides/URI_REPLACEMENT_GUIDE.md)**
  - Replacing URIs during merge
  - URI strategies
  - Content resolution

---

## ⚡ Quick Reference

Fast lookup for common tasks:

- **[quick-reference/MERGE_KEYS_SUMMARY.md](quick-reference/MERGE_KEYS_SUMMARY.md)**
  - Key matching rules
  - Common merge patterns
  - Priority order

- **[quick-reference/MERGE_TUPLE_QUICK_REFERENCE.md](quick-reference/MERGE_TUPLE_QUICK_REFERENCE.md)**
  - Tuple setup examples
  - Verification commands
  - Common patterns

- **[quick-reference/DYNAMIC_TUPLES_QUICK_REF.md](quick-reference/DYNAMIC_TUPLES_QUICK_REF.md)**
  - Dynamic composition
  - Runtime overrides
  - Use cases

- **[quick-reference/URI_REPLACEMENT_SUMMARY.md](quick-reference/URI_REPLACEMENT_SUMMARY.md)**
  - URI replacement patterns
  - Quick examples
  - Best practices

---

## 🎨 Design Documentation

Design decisions and feature documentation:

- **[design/DESIGN_REVIEW_SUMMARY.md](design/DESIGN_REVIEW_SUMMARY.md)**
  - ai_init_methodology project review
  - Design validation
  - Best practices

- **[design/METHODOLOGY_PROJECT_DESIGN_REVIEW.md](design/METHODOLOGY_PROJECT_DESIGN_REVIEW.md)**
  - Complete design review
  - Correct vs incorrect patterns
  - Integration examples

- **[design/FULL_CONTEXT_STATE_FEATURE.md](design/FULL_CONTEXT_STATE_FEATURE.md)**
  - Context state visualization feature
  - Layer transparency
  - Usage documentation

---

## 🗄️ Historical Documentation

Archived/deprecated documentation:

- **[deprecated/AI_INIT_REVIEW.md](deprecated/AI_INIT_REVIEW.md)** - Historical ai_init comparison
- **[deprecated/RENAME_SUMMARY.md](deprecated/RENAME_SUMMARY.md)** - Project rename documentation
- **[deprecated/STATUS.md](deprecated/STATUS.md)** - Outdated project status
- **[deprecated/EXAMPLE_WALKTHROUGH.md](deprecated/EXAMPLE_WALKTHROUGH.md)** - Outdated examples

---

## 📍 Documentation Map

### By Topic

#### Getting Started
- [README.md](../README.md) → Overview
- [QUICKSTART.md](../QUICKSTART.md) → Quick start
- [PLUGIN_GUIDE.md](../PLUGIN_GUIDE.md) → Installation

#### Configuration & Merging
- [guides/MERGE_KEYS_EXPLAINED.md](guides/MERGE_KEYS_EXPLAINED.md) → How merges work
- [guides/CREATING_MERGE_TUPLES.md](guides/CREATING_MERGE_TUPLES.md) → Static tuples
- [guides/DYNAMIC_MERGE_TUPLES.md](guides/DYNAMIC_MERGE_TUPLES.md) → Runtime tuples
- [guides/URI_REPLACEMENT_GUIDE.md](guides/URI_REPLACEMENT_GUIDE.md) → URI handling

#### System Architecture
- [ARCHITECTURE.md](ARCHITECTURE.md) → Technical design
- [MCP_SETUP.md](MCP_SETUP.md) → MCP integration
- [SUBAGENTS_GUIDE.md](SUBAGENTS_GUIDE.md) → Subagents

#### Examples & Usage
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) → Practical examples
- [quick-reference/](quick-reference/) → Quick lookups

### By User Type

#### **New Users**
1. [../README.md](../README.md) - Understand what this is
2. [../QUICKSTART.md](../QUICKSTART.md) - Get it running
3. [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - See examples

#### **Plugin Users**
1. [../PLUGIN_GUIDE.md](../PLUGIN_GUIDE.md) - Install plugin
2. [quick-reference/](quick-reference/) - Quick commands
3. [SUBAGENTS_GUIDE.md](SUBAGENTS_GUIDE.md) - Use subagents

#### **Developers**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand design
2. [guides/](guides/) - Detailed guides
3. [design/](design/) - Design docs

#### **CI/CD Engineers**
1. [guides/DYNAMIC_MERGE_TUPLES.md](guides/DYNAMIC_MERGE_TUPLES.md) - Runtime composition
2. [guides/MERGE_KEYS_EXPLAINED.md](guides/MERGE_KEYS_EXPLAINED.md) - Merge behavior
3. [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Integration examples

---

## 🔍 Finding What You Need

### Common Questions

**"How do I get started?"**
→ [../QUICKSTART.md](../QUICKSTART.md)

**"How do I install the plugin?"**
→ [../PLUGIN_GUIDE.md](../PLUGIN_GUIDE.md)

**"How does merging work?"**
→ [guides/MERGE_KEYS_EXPLAINED.md](guides/MERGE_KEYS_EXPLAINED.md)

**"How do I create an inheritance chain?"**
→ [guides/CREATING_MERGE_TUPLES.md](guides/CREATING_MERGE_TUPLES.md)

**"How do I dynamically compose configurations?"**
→ [guides/DYNAMIC_MERGE_TUPLES.md](guides/DYNAMIC_MERGE_TUPLES.md)

**"How do I replace URIs?"**
→ [guides/URI_REPLACEMENT_GUIDE.md](guides/URI_REPLACEMENT_GUIDE.md)

**"What's the architecture?"**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**"How do I set up MCP?"**
→ [MCP_SETUP.md](MCP_SETUP.md)

**"How do I create subagents?"**
→ [SUBAGENTS_GUIDE.md](SUBAGENTS_GUIDE.md)

---

## 📦 Documentation Structure

```
docs/
├── README.md                           # This file
├── ARCHITECTURE.md                     # Technical architecture
├── MCP_SETUP.md                        # MCP server setup
├── USAGE_EXAMPLES.md                   # Usage examples
├── SUBAGENTS_GUIDE.md                  # Subagents guide
│
├── guides/                             # Detailed how-to guides
│   ├── CREATING_MERGE_TUPLES.md
│   ├── DYNAMIC_MERGE_TUPLES.md
│   ├── MERGE_KEYS_EXPLAINED.md
│   └── URI_REPLACEMENT_GUIDE.md
│
├── quick-reference/                    # Quick lookup guides
│   ├── MERGE_KEYS_SUMMARY.md
│   ├── MERGE_TUPLE_QUICK_REFERENCE.md
│   ├── DYNAMIC_TUPLES_QUICK_REF.md
│   └── URI_REPLACEMENT_SUMMARY.md
│
├── design/                             # Design documentation
│   ├── DESIGN_REVIEW_SUMMARY.md
│   ├── METHODOLOGY_PROJECT_DESIGN_REVIEW.md
│   └── FULL_CONTEXT_STATE_FEATURE.md
│
└── deprecated/                         # Historical/archived docs
    ├── AI_INIT_REVIEW.md
    ├── RENAME_SUMMARY.md
    ├── STATUS.md
    └── EXAMPLE_WALKTHROUGH.md
```

---

## 🤝 Contributing

When adding new documentation:

1. **Guides** → Place in `guides/` with detailed explanations
2. **Quick refs** → Place in `quick-reference/` with concise examples
3. **Design docs** → Place in `design/` with design decisions
4. **Deprecated** → Move outdated docs to `deprecated/`
5. **Update this README** → Add links to new documentation

---

## 📄 License

See [../LICENSE](../LICENSE) for license information.

---

*Last updated: 2025-10-16*
