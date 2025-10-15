# URI Replacement - Quick Guide

## Question: How do I replace a URI?

**Answer**: Define the same key path in a higher-priority layer with a different URI.

**Rule**: Later layers override earlier layers - this applies to URIs too.

---

## Basic Example

```yaml
# Layer 0: Base
methodology:
  principles:
    uri: "file://docs/base_principles.md"

# Layer 1: Override
methodology:
  principles:
    uri: "file://docs/custom_principles.md"  # ← Replaces base URI

# Result:
methodology:
  principles:
    uri: "file://docs/custom_principles.md"  # ✅ Layer 1 wins
```

---

## Common Scenarios

### 1. Replace Documentation Reference

```yaml
Base:     uri: "file://docs/corporate_policy.md"
Override: uri: "file://docs/project_policy.md"
Result:   uri: "file://docs/project_policy.md"  ✅
```

### 2. Switch Between Remote and Local

```yaml
Base:     uri: "https://corporate-wiki.acme.com/standards.md"
Dev:      uri: "file://local/dev_standards.md"
Result:   uri: "file://local/dev_standards.md"  ✅
```

### 3. Replace URI with Inline Data

```yaml
Base:     uri: "file://configs/settings.yml"
Override:
  timeout: 30
  retries: 3
Result:   # ✅ URI replaced with data structure
  timeout: 30
  retries: 3
```

⚠️ **Warning**: This changes the node type from URI to data.

---

## Pattern: _uri + Metadata (Recommended)

```yaml
# Base Layer
principles:
  _uri: "file://docs/SACRED_SEVEN.md"     # Documentation
  count: 7                                  # Metadata
  version: "1.0"

# Override Layer
principles:
  _uri: "file://docs/CUSTOM_PRINCIPLES.md" # ← New documentation
  count: 7                                   # Keep metadata
  version: "2.0"                             # Update version

# Result:
principles:
  _uri: "file://docs/CUSTOM_PRINCIPLES.md" # ✅ New doc
  count: 7
  version: "2.0"                            # ✅ Updated
```

**Why this works**: `_uri` is just another key that merges normally.

---

## Your ai_init_methodology Example

### Current Structure
```yaml
# config.yml
methodology:
  principles:
    _uri: "file://docs/principles/SACRED_SEVEN.md"
    test_driven_development:
      principle: 1
      mantra: "No code without tests"
```

### To Replace the URI
```yaml
# Another project's config
methodology:
  principles:
    _uri: "file://docs/custom_principles.md"  # ← New documentation
    test_driven_development:
      principle: 1
      mantra: "Tests before code, always"     # ← Update mantra if desired
```

### Result
```yaml
methodology:
  principles:
    _uri: "file://docs/custom_principles.md"  # ✅ New URI
    test_driven_development:
      principle: 1
      mantra: "Tests before code, always"     # ✅ Updated mantra
```

---

## How It Works

### Merge Algorithm
```
1. Match key path: "methodology.principles.uri"
2. Compare values:
   - Base: "file://docs/base.md"
   - Override: "file://docs/override.md"
3. Apply OVERRIDE strategy:
   - Result: "file://docs/override.md" (later wins)
```

### Content Resolution
```
1. Merge happens first → Final URI determined
2. Content resolution happens AFTER merge
3. System loads content from the final merged URI
```

**Key insight**: Merge determines WHICH URI, resolution happens LATER.

---

## Use Cases

### Environment-Specific
```yaml
Production: uri: "https://api.production.acme.com/docs"
Development: uri: "https://api.dev.acme.com/docs"
Testing:    uri: "https://api.test.acme.com/docs"
```

### Team-Specific
```yaml
Corporate:  uri: "file://docs/general_onboarding.md"
Team:       uri: "file://docs/payments_team_onboarding.md"
```

### Version-Specific
```yaml
Latest:  uri: "file://docs/python/3.12/guide.md"
Legacy:  uri: "file://docs/python/3.9/guide.md"
```

---

## Best Practices

### ✅ DO
```yaml
# Use consistent URI key naming
_uri: "file://docs/content.md"

# Keep URI + metadata together
section:
  _uri: "file://docs/section.md"
  version: "1.0"
  mandatory: true

# Document why URI was replaced
# Using custom principles for payments security
uri: "file://docs/payment_principles.md"
```

### ❌ DON'T
```yaml
# Don't mix URI and data types carelessly
base:     uri: "file://config.yml"
override: data: {key: value}  # ❌ Type changed, might break code

# Don't use ambiguous relative paths
uri: "docs/file.md"  # ❌ Relative to what?
uri: "file://docs/file.md"  # ✅ Clear scheme
```

---

## Quick Reference

| Scenario | Base Layer | Override Layer | Result |
|----------|-----------|----------------|--------|
| Replace URI | `uri: "file://a.md"` | `uri: "file://b.md"` | `uri: "file://b.md"` ✅ |
| Add metadata | `uri: "file://a.md"` | `version: "2.0"` | `uri: "file://a.md"`<br>`version: "2.0"` ✅ |
| Replace with data | `uri: "file://a.md"` | `key: value` | `key: value` ✅ |
| Keep base URI | `uri: "file://a.md"` | *(omit uri key)* | `uri: "file://a.md"` ✅ |

---

## Verify URI Replacement

### Using /show-full-context
```bash
/load-context my_project
/show-full-context

# Look for:
## Materialized Context (Merged Configuration)
...
uri: "file://docs/final_uri.md"  # ← Shows which URI won
```

### Using ConfigManager
```python
manager.merge()
final_uri = manager.get_uri("methodology.principles")
print(final_uri)  # Shows: "file://docs/final_uri.md"
```

---

## Key Takeaway

**URIs are just values** - they follow the same merge rules as any other value:
- Match on key path
- Later layer wins (OVERRIDE strategy)
- Complete replacement (not partial)
- Resolution happens AFTER merge

**To replace a URI**: Just define it in a higher-priority layer! 🎯

---

*Full details: [URI_REPLACEMENT_GUIDE.md](URI_REPLACEMENT_GUIDE.md)*
