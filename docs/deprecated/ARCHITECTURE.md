# ai_sdlc_method Architecture

## Design Philosophy

ai_sdlc_method is inspired by the C4H configuration system (`c4h/config/system_config.yml` and `c4h_agents/config.py`) but designed to be:

1. **Generic** - No C4H-specific logic; works with any domain
2. **URI-based** - Content lives at URIs, not embedded in config files
3. **Content-agnostic** - Works with any content type (Markdown, JSON, HTML, etc.)
4. **Extensible** - Easy to add custom URI schemes

## Core Components

### 1. HierarchyNode (`models/hierarchy_node.py`)

The fundamental data structure representing nodes in the configuration tree.

**Inspired by**: C4H's `ConfigNode` class (`c4h_agents/config.py:17-165`)

**Key differences**:
- Supports `URIReference` as a value type (not in C4H)
- Tracks `source` and `priority` for merge provenance
- Explicit `path` attribute for each node

```python
@dataclass
class HierarchyNode:
    path: str                           # e.g., "system.agents.discovery"
    value: Optional[NodeValue] = None   # Can be URIReference
    children: Dict[str, HierarchyNode]  # Nested structure
    source: Optional[str] = None        # Which config file
    priority: int = 0                   # Merge priority
```

**Methods**:
- `get_value_by_path(path)` - Similar to C4H's `ConfigNode.get_value()`
- `get_node_by_path(path)` - Similar to C4H's `ConfigNode.get_node()`
- `find_all_by_pattern(pattern)` - Similar to C4H's `ConfigNode.find_all()`

### 2. URIReference (`models/hierarchy_node.py`)

Represents a reference to external content.

**This is the key innovation** - C4H embeds content directly, we reference it.

```python
@dataclass
class URIReference:
    uri: str                            # e.g., "file:///prompts/discovery.md"
    scheme: URIScheme                   # file, http, https, data, ref
    content_type: Optional[str] = None  # MIME type
    metadata: Dict[str, Any]            # version, checksum, etc.
```

**Supported schemes**:
- `file://` - Local filesystem
- `http://`, `https://` - Web resources
- `data:` - Inline data URIs
- `ref:` - Cross-references to other nodes
- Custom schemes via registration

### 3. HierarchyMerger (`mergers/hierarchy_merger.py`)

Merges multiple hierarchies with priority rules.

**Inspired by**: C4H's `deep_merge()` function (`c4h_agents/config.py:304-378`)

**Key similarities**:
- Recursive merging of nested structures
- Later configs override earlier ones
- Deep copy to prevent mutation

**Key differences**:
- Works with `HierarchyNode` objects, not raw dicts
- Preserves `URIReference` objects (doesn't resolve them)
- Tracks merge provenance (source, priority)
- Pluggable merge strategies

```python
class MergeStrategy(Enum):
    OVERRIDE = "override"            # C4H default behavior
    URI_PRIORITY = "uri_priority"    # URIs take precedence
    DEEP_MERGE = "deep_merge"        # Recursive merge
```

**Merge algorithm** (similar to C4H):
```python
def merge(hierarchies: List[HierarchyNode]) -> HierarchyNode:
    result = copy.deepcopy(hierarchies[0])
    for hierarchy in hierarchies[1:]:
        result = _merge_two_nodes(result, hierarchy)
    return result
```

### 4. YAMLLoader (`loaders/yaml_loader.py`)

Loads YAML files into `HierarchyNode` structures.

**Inspired by**: C4H's `load_config()` (`c4h_agents/config.py:380-396`)

**Key difference**: Detects and converts URI strings to `URIReference` objects

**URI detection**:
```yaml
# Detected as URIReference
prompt: "file:///prompts/discovery.md"

# Also detected
prompt:
  uri: "https://docs.example.com/prompt"
  content_type: "text/markdown"
  version: "1.0"
```

### 5. URIResolver (`loaders/uri_resolver.py`)

Resolves URI references to actual content.

**This has no C4H equivalent** - C4H doesn't need resolution since content is embedded.

**Capabilities**:
- Lazy loading (only resolve when accessed)
- Caching (avoid repeated fetches)
- Custom resolvers (extend with your own schemes)

```python
class URIResolver:
    def resolve(self, uri_ref: URIReference) -> str:
        # Route to appropriate resolver
        if uri_ref.scheme == URIScheme.FILE:
            return self._resolve_file(uri_ref)
        elif uri_ref.scheme == URIScheme.HTTP:
            return self._resolve_http(uri_ref)
        # ... etc
```

### 6. ConfigManager (`core/config_manager.py`)

High-level API that combines all components.

**Similar to**: How C4H uses configs in `c4h_services/src/api/service.py`

**Usage pattern comparison**:

**C4H approach** (`service.py:310-319`):
```python
# C4H: Merge embedded configs
config = deepcopy(app.state.default_config)
if request.system_config:
    config = deep_merge(config, request.system_config)
if request.app_config:
    config = deep_merge(config, request.app_config)
```

**ai_sdlc_method approach**:
```python
# ai_sdlc_method: Merge URI-based configs
manager = ConfigManager()
manager.load_hierarchy("base.yml")
manager.load_hierarchy("production.yml")
manager.add_runtime_overrides({...})
manager.merge()
```

## Configuration Flow

### Loading Phase

```
┌─────────────────────────────────────────────────────┐
│ 1. YAML File(s)                                     │
│    - base.yml                                       │
│    - production.yml                                 │
│    - development.yml                                │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ YAMLLoader.load()
                   ↓
┌─────────────────────────────────────────────────────┐
│ 2. HierarchyNode Trees (separate)                  │
│    - Each file becomes a separate tree              │
│    - URI strings converted to URIReference          │
│    - Structure preserved                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ HierarchyMerger.merge()
                   ↓
┌─────────────────────────────────────────────────────┐
│ 3. Single Merged HierarchyNode                     │
│    - All trees merged into one                      │
│    - Priority rules applied                         │
│    - URIReferences preserved (not resolved)         │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Access via dot notation
                   ↓
┌─────────────────────────────────────────────────────┐
│ 4. Value or URIReference                           │
│    - Direct value: return immediately               │
│    - URIReference: defer to resolver                │
└─────────────────────────────────────────────────────┘
```

### Resolution Phase (on-demand)

```
┌─────────────────────────────────────────────────────┐
│ User calls get_content(path)                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ ConfigManager
                   ↓
┌─────────────────────────────────────────────────────┐
│ Get value at path                                   │
│   - Is it a URIReference?                           │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Yes → URIResolver.resolve()
                   ↓
┌─────────────────────────────────────────────────────┐
│ Fetch content from URI                              │
│   - file:// → read local file                       │
│   - https:// → HTTP GET request                     │
│   - ref: → lookup other node                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│ Return content string                               │
└─────────────────────────────────────────────────────┘
```

## Comparison with C4H

### Similarities

| Feature | C4H | ai_sdlc_method |
|---------|-----|----------------|
| Dot notation | ✅ `config.get_value("llm_config.agents.discovery")` | ✅ `manager.get_value("llm.agents.discovery")` |
| Wildcard search | ✅ `config.find_all("*.agents.*")` | ✅ `manager.find_all("*.agents.*")` |
| Priority merging | ✅ `deep_merge(base, override)` | ✅ `merger.merge([base, override])` |
| Hierarchical structure | ✅ YAML nesting | ✅ YAML nesting → HierarchyNode tree |
| Multiple configs | ✅ System + App configs | ✅ Base + Env + Runtime configs |

### Differences

| Aspect | C4H | ai_sdlc_method |
|--------|-----|----------------|
| **Content storage** | Embedded in YAML | Referenced by URI |
| **Content types** | YAML values only | Any content at any URI |
| **Content loading** | Eager (all loaded) | Lazy (loaded on access) |
| **Versioning** | Config + content together | Config separate from content |
| **Updates** | Redeploy to change | Update content at URI |
| **Domain** | LLM/agent specific | Generic, any domain |
| **Dependencies** | Coupled to C4H | Standalone library |

### Example: Prompts

**C4H approach**:
```yaml
llm_config:
  agents:
    solution_designer:
      prompts:
        system: |
          You are a code modification solution designer...
          [100 lines of embedded text]
```

**ai_sdlc_method approach**:
```yaml
llm:
  agents:
    solution_designer:
      prompts:
        system: "file://prompts/solution_designer.md"
        # or: "https://docs.company.com/prompts/v2/solution_designer"
```

**Benefits**:
1. Config file stays small and readable
2. Prompt can be edited without touching config
3. Prompt can live on web server (easy updates)
4. Prompt can be versioned separately (Git submodule)
5. Same prompt can be referenced from multiple configs

## Merge Priority Examples

### Three-Layer Merge

**Similar to C4H's API merging** (`service.py:310-319`):

```python
# Layer 1: Base defaults (lowest priority)
base.yml:
  llm:
    agents:
      discovery:
        model: "claude-3-opus"
        temperature: 0

# Layer 2: Environment override
production.yml:
  llm:
    agents:
      discovery:
        model: "claude-3-7-sonnet"  # Overrides base

# Layer 3: Runtime override (highest priority)
runtime_overrides = {
    "llm.agents.discovery.temperature": 0.5  # Overrides base
}

# Result after merge:
merged = {
    "llm": {
        "agents": {
            "discovery": {
                "model": "claude-3-7-sonnet",     # From production
                "temperature": 0.5                # From runtime
            }
        }
    }
}
```

### URI Priority Strategy

```python
# Base config
base = {
    "prompt": URIReference("file://prompts/base.md")
}

# Override config (trying to replace with direct value)
override = {
    "prompt": "Simple inline prompt"
}

# With URI_PRIORITY strategy:
merged = {
    "prompt": URIReference("file://prompts/base.md")  # URI wins
}

# With OVERRIDE strategy (default):
merged = {
    "prompt": "Simple inline prompt"  # Override wins
}
```

## Extension Points

### Custom URI Schemes

Register resolvers for custom schemes:

```python
# Example: Environment variable resolver
def resolve_env(uri_ref: URIReference) -> str:
    var_name = uri_ref.uri.replace("env://", "")
    return os.environ.get(var_name, "")

manager.register_uri_resolver("env", resolve_env)

# Now can use env:// in configs
config.yml:
  api:
    key: "env://API_KEY"
```

**Other potential schemes**:
- `s3://bucket/key` - AWS S3
- `vault://secret/path` - HashiCorp Vault
- `git://repo/file@branch` - Git repository
- `db://table/column/id` - Database content

### Custom Merge Strategies

Extend `MergeStrategy` for domain-specific rules:

```python
class CustomMergeStrategy(MergeStrategy):
    KEEP_LONGEST = "keep_longest"  # Keep longer value
    CONCATENATE = "concatenate"     # Combine values
```

## Use Cases

### 1. Multi-Environment Configuration

```
configs/
  base.yml              # Common defaults
  development.yml       # Dev overrides
  staging.yml          # Staging overrides
  production.yml       # Production overrides

manager.load_hierarchy("configs/base.yml")
manager.load_hierarchy(f"configs/{env}.yml")
```

### 2. Distributed Documentation

```yaml
docs:
  api_reference: "https://docs.company.com/api/v2/reference"
  user_guide: "https://docs.company.com/guides/user"
  troubleshooting: "https://internal.wiki/troubleshooting"
```

### 3. Prompt Management

```yaml
agents:
  discovery:
    prompt: "https://prompts.company.com/discovery/v3"
  coder:
    prompt: "https://prompts.company.com/coder/v2"
```

Update prompts without redeploying code!

### 4. Content Sharing

```yaml
common:
  disclaimer: "file://legal/disclaimer.md"

pages:
  home:
    footer: "ref:common.disclaimer"  # Reuse content
  about:
    footer: "ref:common.disclaimer"  # Same content
```

## Performance Considerations

### Lazy Loading

Content is only loaded when `get_content()` is called, not during merge.

```python
# Fast - only loads structure
manager.merge()

# Slow - fetches from URI
content = manager.get_content("agent.prompt")
```

### Caching

URIResolver caches fetched content:

```python
# First call: fetch from URI
content1 = manager.get_content("agent.prompt")

# Second call: return from cache
content2 = manager.get_content("agent.prompt")
```

### Deep Copy Overhead

Similar issue to C4H - merge does deep copy of trees.

**Mitigation**: Only merge when needed, reuse merged hierarchy.

## Future Enhancements

1. **Async resolution** - Fetch multiple URIs in parallel
2. **Content validation** - Schema validation for content
3. **Cache persistence** - Save fetched content to disk
4. **Diff/patch** - Show what changed between merges
5. **Import/export** - Convert to other formats (JSON, TOML)
6. **Visual tools** - GUI for exploring hierarchy
7. **Hot reload** - Watch URIs for changes
8. **Encryption** - Encrypted content at URIs

## Summary

ai_sdlc_method takes the elegant design of C4H's configuration system and extends it to work with **content at any URI**, making it:

- ✅ **Generic** - Not tied to any specific domain
- ✅ **Flexible** - Content can live anywhere
- ✅ **Scalable** - Lazy loading, caching
- ✅ **Maintainable** - Separate structure from content
- ✅ **Extensible** - Custom URI schemes and strategies

It preserves the core strengths of C4H (dot notation, priority merging, structured access) while adding URI-based content management as a first-class concept.
