# URI Replacement in Merges

## Quick Answer

**To replace a URI**: Simply define the same key path in a higher-priority layer with a different URI.

**The merge rule**: Later layers override earlier layers - this applies to URIs too.

---

## Basic URI Replacement

### Example 1: Replace URI with Different URI

```yaml
# Layer 0: Corporate Base
methodology:
  principles:
    uri: "file://docs/corporate/principles.md"

# Layer 1: Project-Specific
methodology:
  principles:
    uri: "file://docs/project/custom_principles.md"  # ← Replaces corporate URI

# Result after merge:
methodology:
  principles:
    uri: "file://docs/project/custom_principles.md"  # ✅ Layer 1 wins
```

**What happens**:
- Corporate principles URI is completely replaced
- Project-specific principles URI is used
- When content is resolved, it loads from the project file

---

## URI Replacement Scenarios

### Scenario 1: Override Documentation Reference

```yaml
# Base Layer
corporate:
  policies:
    security:
      uri: "file://docs/policies/corporate_security_policy.md"
      version: "2.1"
      mandatory: true

# Project Layer
corporate:
  policies:
    security:
      uri: "file://docs/policies/payment_security_policy.md"  # ← Custom policy
      version: "3.0"
      mandatory: true

# Result:
corporate:
  policies:
    security:
      uri: "file://docs/policies/payment_security_policy.md"  # ✅ New URI
      version: "3.0"                                            # ✅ New version
      mandatory: true                                           # ✅ Unchanged
```

### Scenario 2: Replace HTTP URI with Local File

```yaml
# Base Layer
methodology:
  coding_standards:
    uri: "https://corporate-wiki.acme.com/standards/python.md"

# Development Layer (runtime override)
methodology:
  coding_standards:
    uri: "file://local/dev_standards.md"  # ← Use local version during dev

# Result:
methodology:
  coding_standards:
    uri: "file://local/dev_standards.md"  # ✅ Local file used
```

### Scenario 3: Replace URI with Inline Data

```yaml
# Base Layer
configuration:
  settings:
    uri: "file://configs/default_settings.yml"

# Override Layer
configuration:
  settings:              # ← No URI, replace with direct data
    timeout: 30
    retries: 3
    enabled: true

# Result:
configuration:
  settings:             # ✅ URI replaced with inline data
    timeout: 30
    retries: 3
    enabled: true
```

**Warning**: This changes the node from a URI reference to a data container.

---

## Advanced: URI with Structured Data

### Pattern: _uri + Structured Data (Recommended)

```yaml
# Base Layer
methodology:
  principles:
    _uri: "file://docs/principles/SACRED_SEVEN.md"  # Full documentation
    test_driven_development:                         # Structured metadata
      principle: 1
      mantra: "No code without tests"

# Override Layer
methodology:
  principles:
    _uri: "file://docs/principles/CUSTOM_PRINCIPLES.md"  # ← New documentation
    test_driven_development:                              # Keep metadata
      principle: 1
      mantra: "Tests before code, always"                 # ← Updated mantra

# Result:
methodology:
  principles:
    _uri: "file://docs/principles/CUSTOM_PRINCIPLES.md"  # ✅ New documentation
    test_driven_development:
      principle: 1
      mantra: "Tests before code, always"                # ✅ Updated mantra
```

**Why this works**:
- `_uri` is just another key that merges normally
- Structured data merges separately
- You can replace documentation while keeping/updating metadata

---

## Common Use Cases

### Use Case 1: Environment-Specific URIs

```yaml
# Base configuration
external_services:
  api_docs:
    uri: "https://api.production.acme.com/docs"

# Development override
external_services:
  api_docs:
    uri: "https://api.dev.acme.com/docs"  # ← Dev environment

# Testing override
external_services:
  api_docs:
    uri: "https://api.test.acme.com/docs"  # ← Test environment
```

### Use Case 2: Team-Specific Documentation

```yaml
# Corporate base
team_guides:
  onboarding:
    uri: "file://docs/onboarding/general_onboarding.md"

# Team-specific
team_guides:
  onboarding:
    uri: "file://docs/onboarding/payments_team_onboarding.md"  # ← Team-specific
```

### Use Case 3: Version-Specific References

```yaml
# Base: Latest version
dependencies:
  python_guide:
    uri: "file://docs/python/3.12/guide.md"

# Override: Specific version for legacy project
dependencies:
  python_guide:
    uri: "file://docs/python/3.9/guide.md"  # ← Older version
```

---

## How URI Replacement Works Internally

### Merge Algorithm

From `hierarchy_merger.py`:

```python
# If override is a leaf node with value, it wins
if override.is_leaf() and override.value is not None:
    if self.strategy == MergeStrategy.OVERRIDE:
        result.value = copy.deepcopy(override.value)  # ← URI replaced here
        result.source = override.source
        result.priority = priority
```

**What this means**:
1. URI is treated as a regular value
2. Later layer's URI completely replaces earlier layer's URI
3. No special URI-merging logic (by default)

### URI Priority Strategy (Alternative)

There's also a `URI_PRIORITY` strategy:

```python
elif self.strategy == MergeStrategy.URI_PRIORITY:
    # If override has URI, it wins
    if isinstance(override.value, URIReference):
        result.value = copy.deepcopy(override.value)
    # If base has URI and override doesn't, base wins
    elif not isinstance(result.value, URIReference):
        result.value = copy.deepcopy(override.value)
    # Else: base has URI, override doesn't -> keep base
```

**Behavior**:
- URIs always take priority over non-URI values
- If both have URIs, later wins (same as OVERRIDE)
- If only base has URI, keep the URI (don't replace with non-URI data)

---

## Access URIs After Merge

### Via ConfigManager

```python
from ai_sdlc_config import ConfigManager

manager = ConfigManager()
manager.load_hierarchy("01_base.yml")
manager.load_hierarchy("02_override.yml")
manager.merge()

# Get the URI
uri = manager.get_uri("methodology.principles")
# Returns: "file://docs/principles/CUSTOM_PRINCIPLES.md"

# Get the content from the URI
content = manager.get_content("methodology.principles")
# Returns: Full content from the resolved URI
```

### Via ContextManager (MCP)

```python
context = context_manager.load_context("my_project")

# URIs are resolved during context loading
policies = context["policies"]
# Contains resolved policy content
```

---

## Best Practices

### ✅ DO: Use Consistent URI Keys

```yaml
# Good: Consistent _uri key pattern
section:
  _uri: "file://docs/section.md"
  metadata:
    key: value

# Also good: uri key pattern
section:
  uri: "file://docs/section.md"
  version: "1.0"
```

### ✅ DO: Keep URI + Metadata Together

```yaml
# Good: URI with metadata
principles:
  _uri: "file://docs/SACRED_SEVEN.md"
  count: 7
  version: "1.0"
  mandatory: true
```

### ✅ DO: Document URI Replacements

```yaml
# Good: Comment why URI was replaced
methodology:
  principles:
    # Using project-specific principles instead of corporate
    # because payments require additional security principles
    uri: "file://docs/payment_principles.md"
```

### ❌ DON'T: Mix URI Types Carelessly

```yaml
# Problematic: Switching between URI and data
base:
  config:
    uri: "file://config.yml"

override:
  config:              # ← Now it's data, not a URI reference
    setting1: value1
    setting2: value2

# Later code expecting a URI will break!
```

### ❌ DON'T: Use Relative Paths Without Context

```yaml
# Problematic: Relative to what?
principles:
  uri: "docs/principles.md"  # ❌ Ambiguous

# Better: Explicit scheme
principles:
  uri: "file://docs/principles.md"  # ✅ Clear it's a file URI
```

---

## URI Schemes Supported

From the system:

```python
class URIScheme(Enum):
    FILE = "file"         # file://path/to/file
    HTTP = "http"         # http://example.com/resource
    HTTPS = "https"       # https://example.com/resource
    DATA = "data"         # data:text/plain;base64,SGVsbG8=
    REF = "ref"          # ref://internal/reference
```

### Examples of Each Scheme

```yaml
# File URI
local_docs:
  uri: "file://docs/local_file.md"

# HTTPS URI
remote_docs:
  uri: "https://docs.acme.com/api_spec.yml"

# Data URI (inline)
inline_config:
  uri: "data:text/plain;base64,Y29uZmlnOnZhbHVl"

# Reference URI (internal)
shared_config:
  uri: "ref://configs/shared_settings"
```

---

## Testing URI Replacement

### Verify URI Was Replaced

```python
# Load and merge
manager.load_hierarchy("base.yml")
manager.load_hierarchy("override.yml")
manager.merge()

# Verify the URI
final_uri = manager.get_uri("methodology.principles")
assert final_uri == "file://docs/override_principles.md"

# Verify the content comes from new URI
content = manager.get_content("methodology.principles")
assert "Override Principles" in content
```

---

## Real-World Example: ai_init_methodology

Your methodology project uses URIs effectively:

```yaml
# config.yml
methodology:
  principles:
    _uri: "file://docs/principles/SACRED_SEVEN.md"  # ← Full documentation

    test_driven_development:          # ← Structured data
      principle: 1
      mantra: "No code without tests"
      workflow: RED → GREEN → REFACTOR

  processes:
    tdd_workflow:
      _uri: "file://docs/processes/TDD_WORKFLOW.md"  # ← Full documentation

      cycle:                          # ← Structured data
        - phase: RED
          action: Write failing test first
```

**To override these URIs**, a project would:

```yaml
# project_config.yml
methodology:
  principles:
    _uri: "file://docs/custom_principles.md"  # ← Replace with custom principles
    # Keep the structured data or override it too

  processes:
    tdd_workflow:
      _uri: "file://docs/custom_workflow.md"  # ← Replace with custom workflow
```

---

## Summary

### URI Replacement Rules

1. **Same as any value**: URIs merge using the same rules as other values
2. **Later wins**: Higher priority layer's URI replaces lower priority layer's URI
3. **Complete replacement**: Old URI is completely discarded
4. **Path-based**: Match on the same key path to replace

### Quick Examples

```yaml
# Replace URI with URI
base:    uri: "file://docs/base.md"
override: uri: "file://docs/override.md"
result:   uri: "file://docs/override.md"  # ✅

# Replace URI with data
base:    uri: "file://docs/base.md"
override: data: {key: value}
result:   data: {key: value}  # ✅ (but changes type!)

# Add URI where none existed
base:    data: {key: value}
override: uri: "file://docs/new.md"
result:   uri: "file://docs/new.md"  # ✅
```

### Key Insight

**URIs are just values** - they follow the same merge rules as everything else. The magic is that the content resolution happens AFTER merging, so the merged URI is what gets resolved.

---

## Questions?

**Q: Can I partially replace a URI (e.g., just the filename)?**
A: No, URIs are atomic values. You replace the entire URI string.

**Q: What if I want to keep the base URI but add metadata?**
A: Add the metadata in the override layer without specifying the URI:
```yaml
override:
  principles:
    # Don't specify uri - it stays from base
    version: "2.0"  # Add metadata
```

**Q: How do I know which layer's URI won?**
A: Use `get_full_context_state()` to see layer attribution:
```bash
/show-full-context
```

**Q: Can I use environment variables in URIs?**
A: Yes, if you implement an `env://` URI scheme resolver:
```yaml
uri: "env://DOCS_BASE_URL/principles.md"
```

---

*See also: [MERGE_KEYS_EXPLAINED.md](MERGE_KEYS_EXPLAINED.md) for general merge behavior*
