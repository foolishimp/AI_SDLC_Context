# AI_SDLC_Context Test Suite

This directory contains comprehensive unit tests for the AI_SDLC_Context library.

## Test Coverage

The test suite includes **156 test cases** covering all major components:

### 1. `test_hierarchy_node.py` (51 tests)
Tests for the core data model (`HierarchyNode`, `URIReference`):
- **URIScheme enum** - All supported URI schemes
- **URIReference** - Creation, parsing, string conversion
- **HierarchyNode basics** - Creation, children, leaf/container detection
- **Path navigation** - `get_value_by_path()`, `get_node_by_path()`
- **Pattern matching** - `find_all_by_pattern()` with wildcards
- **Serialization** - `to_dict()` conversion
- **Various value types** - Strings, numbers, booleans, lists, dicts, URIs

### 2. `test_yaml_loader.py` (28 tests)
Tests for YAML configuration loading:
- **Basic loading** - Files, strings, empty files
- **URI detection** - Automatic detection of file://, https://, http://, data:, ref: URIs
- **URI reference dicts** - Dict format with uri/ref keys and metadata
- **Nested structures** - Deep nesting, lists, complex hierarchies
- **Primitive types** - Strings, integers, floats, booleans, null
- **YAML features** - Anchors and aliases
- **Path construction** - Correct dot-delimited paths
- **Error handling** - Invalid YAML, missing files

### 3. `test_uri_resolver.py` (28 tests)
Tests for URI content resolution:
- **File URIs** - Absolute paths, relative paths, nested directories
- **HTTP/HTTPS URIs** - Web resource fetching (mocked)
- **Data URIs** - Plain text, base64 encoding, media types
- **Ref URIs** - Cross-references within hierarchy, recursive resolution
- **Custom resolvers** - Registration and usage of custom URI schemes
- **Caching** - Content caching and cache clearing
- **Error handling** - File not found, network errors, invalid formats
- **Edge cases** - Unicode, empty files, circular references

### 4. `test_hierarchy_merger.py` (31 tests)
Tests for configuration merging:
- **Merge strategies** - OVERRIDE, PRESERVE, URI_PRIORITY, DEEP_MERGE
- **Basic merging** - Two hierarchies, multiple hierarchies
- **Priority handling** - Later configs override earlier ones
- **Nested structures** - Deep recursive merging
- **URI references** - Preserving URIs during merge
- **Container/leaf transformations** - Converting between types
- **Runtime overrides** - Dynamic path-based overrides
- **Source tracking** - Preserving config file origins
- **Conflict resolution** - Multiple children, complex scenarios
- **Immutability** - Original hierarchies not mutated
- **MergeReport** - Merge operation reporting

### 5. `test_config_manager.py` (18 tests)
Tests for the high-level API:
- **Manager creation** - Base path, merge strategy configuration
- **Loading** - Files, strings, relative/absolute paths
- **Runtime overrides** - Adding dynamic configuration
- **Merging** - Multi-layer merge operations
- **Value access** - `get_value()`, `get_uri()`, `get_content()`
- **Node access** - `get_node()` for tree exploration
- **Pattern matching** - `find_all()` with wildcards
- **Serialization** - `to_dict()` conversion
- **Custom resolvers** - Registering URI scheme handlers
- **Integration scenarios** - Complex multi-environment configurations
- **Error handling** - Proper error propagation

## Running Tests

### Install Dependencies
```bash
pip install -r tests/requirements.txt
```

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_hierarchy_node.py -v
```

### Run Specific Test
```bash
pytest tests/test_hierarchy_node.py::TestHierarchyNode::test_create_empty_node -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=src/ai_sdlc_config --cov-report=html
```

### Run Tests in Parallel
```bash
pytest tests/ -n auto
```

## Test Structure

Each test file follows this structure:
- **Fixtures** - Reusable test data and setup
- **Test classes** - Grouped by component or functionality
- **Test methods** - Individual test cases with descriptive names

### Naming Conventions
- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<what_is_being_tested>`

### Assertions
Tests use descriptive assertions with clear failure messages:
```python
assert actual == expected, f"Expected {expected}, got {actual}"
```

## Test Configuration

### pytest.ini
- Test discovery patterns
- Output formatting
- Markers for categorizing tests
- Coverage options (commented out by default)

### Test Requirements
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking support
- `pytest-xdist` - Parallel test execution
- `pytest-timeout` - Test timeouts
- `pytest-asyncio` - Async test support

## Key Test Patterns

### 1. Fixture-based Setup
```python
@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
```

### 2. Parametrized Tests
For testing multiple scenarios with the same logic:
```python
@pytest.mark.parametrize("value,expected", [
    ("string", str),
    (42, int),
    (3.14, float),
])
def test_value_types(value, expected):
    assert isinstance(value, expected)
```

### 3. Exception Testing
```python
with pytest.raises(ValueError, match="specific error message"):
    problematic_function()
```

### 4. Mock External Dependencies
```python
@patch('urllib.request.urlopen')
def test_http_fetch(mock_urlopen):
    mock_urlopen.return_value = mock_response
    # Test code here
```

## Test Results Summary

**Total Tests**: 156
**Passing**: 156 (100%)
**Failing**: 0
**Execution Time**: ~0.16 seconds

All tests pass successfully, providing comprehensive coverage of:
- Core data structures
- Configuration loading
- URI resolution
- Merge operations
- High-level API
- Error handling
- Edge cases

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add tests for edge cases
4. Update this README if adding new test categories

## Future Enhancements

Potential test additions:
- Performance benchmarks
- Integration tests with real files
- Property-based testing with Hypothesis
- Stress tests with large hierarchies
- Concurrent access tests
