"""
Unit tests for hierarchy_node module.

# Validates: REQ-NFR-FEDERATE-001 (Hierarchical configuration composition)
# Validates: REQ-NFR-CONTEXT-001 (Persistent context structure)

Tests cover:
- URIScheme enum
- URIReference creation and parsing
- HierarchyNode basic operations
- Path navigation (get_value_by_path, get_node_by_path)
- Wildcard pattern matching (find_all_by_pattern)
- Tree structure operations
"""
import pytest
from ai_sdlc_config.models.hierarchy_node import (
    URIScheme,
    URIReference,
    HierarchyNode,
    NodeValue
)


class TestURIScheme:
    """Test URIScheme enum"""

    def test_all_schemes_exist(self):
        """Verify all expected URI schemes are defined"""
        assert URIScheme.FILE.value == "file"
        assert URIScheme.HTTP.value == "http"
        assert URIScheme.HTTPS.value == "https"
        assert URIScheme.DATA.value == "data"
        assert URIScheme.REF.value == "ref"


class TestURIReference:
    """Test URIReference class"""

    def test_create_uri_reference_file(self):
        """Test creating a file:// URI reference"""
        uri_ref = URIReference(
            uri="file:///path/to/file.txt",
            scheme=URIScheme.FILE
        )
        assert uri_ref.uri == "file:///path/to/file.txt"
        assert uri_ref.scheme == URIScheme.FILE
        assert uri_ref.content_type is None
        assert uri_ref.metadata == {}

    def test_create_uri_reference_with_metadata(self):
        """Test creating URI reference with content type and metadata"""
        uri_ref = URIReference(
            uri="https://example.com/doc.md",
            scheme=URIScheme.HTTPS,
            content_type="text/markdown",
            metadata={"version": "1.0", "checksum": "abc123"}
        )
        assert uri_ref.content_type == "text/markdown"
        assert uri_ref.metadata["version"] == "1.0"
        assert uri_ref.metadata["checksum"] == "abc123"

    def test_from_string_with_file_scheme(self):
        """Test parsing file:// URI from string"""
        uri_ref = URIReference.from_string("file:///prompts/discovery.md")
        assert uri_ref.uri == "file:///prompts/discovery.md"
        assert uri_ref.scheme == URIScheme.FILE

    def test_from_string_with_https_scheme(self):
        """Test parsing https:// URI from string"""
        uri_ref = URIReference.from_string("https://docs.example.com/prompt")
        assert uri_ref.uri == "https://docs.example.com/prompt"
        assert uri_ref.scheme == URIScheme.HTTPS

    def test_from_string_without_scheme(self):
        """Test parsing URI without scheme defaults to file://"""
        uri_ref = URIReference.from_string("/path/to/file.txt")
        assert uri_ref.uri == "file:///path/to/file.txt"
        assert uri_ref.scheme == URIScheme.FILE

    def test_from_string_unsupported_scheme(self):
        """Test that unsupported scheme raises ValueError"""
        with pytest.raises(ValueError, match="Unsupported URI scheme"):
            URIReference.from_string("ftp://example.com/file")

    def test_uri_reference_repr(self):
        """Test string representation of URIReference"""
        uri_ref = URIReference.from_string("file:///test.txt")
        assert repr(uri_ref) == "URIReference(uri='file:///test.txt')"


class TestHierarchyNode:
    """Test HierarchyNode class"""

    def test_create_empty_node(self):
        """Test creating an empty hierarchy node"""
        node = HierarchyNode(path="system")
        assert node.path == "system"
        assert node.value is None
        assert node.children == {}
        assert node.source is None
        assert node.priority == 0
        assert node.metadata == {}

    def test_create_leaf_node_with_value(self):
        """Test creating a leaf node with a value"""
        node = HierarchyNode(
            path="system.name",
            value="MyApp",
            source="base.yml"
        )
        assert node.value == "MyApp"
        assert node.source == "base.yml"
        assert node.is_leaf()
        assert not node.is_container()

    def test_create_node_with_uri_reference(self):
        """Test creating a node with URI reference value"""
        uri_ref = URIReference.from_string("file:///prompts/test.md")
        node = HierarchyNode(path="prompt", value=uri_ref)
        assert node.is_uri_reference()
        assert node.value.uri == "file:///prompts/test.md"

    def test_add_child(self):
        """Test adding child nodes"""
        parent = HierarchyNode(path="system")
        child = HierarchyNode(path="system.name", value="MyApp")
        parent.add_child("name", child)

        assert "name" in parent.children
        assert parent.children["name"] == child
        assert parent.is_container()
        assert not parent.is_leaf()

    def test_get_child(self):
        """Test getting immediate child by key"""
        parent = HierarchyNode(path="system")
        child = HierarchyNode(path="system.name", value="MyApp")
        parent.add_child("name", child)

        retrieved = parent.get_child("name")
        assert retrieved == child

        none_child = parent.get_child("nonexistent")
        assert none_child is None

    def test_get_value_by_path_single_level(self):
        """Test getting value by single-level path"""
        parent = HierarchyNode(path="system")
        child = HierarchyNode(path="system.name", value="MyApp")
        parent.add_child("name", child)

        value = parent.get_value_by_path("name")
        assert value == "MyApp"

    def test_get_value_by_path_nested(self):
        """Test getting value by nested path"""
        root = HierarchyNode(path="")
        system = HierarchyNode(path="system")
        agents = HierarchyNode(path="system.agents")
        discovery = HierarchyNode(path="system.agents.discovery")
        model = HierarchyNode(path="system.agents.discovery.model", value="claude-3-5-sonnet")

        root.add_child("system", system)
        system.add_child("agents", agents)
        agents.add_child("discovery", discovery)
        discovery.add_child("model", model)

        value = root.get_value_by_path("system.agents.discovery.model")
        assert value == "claude-3-5-sonnet"

    def test_get_value_by_path_not_found(self):
        """Test getting value by non-existent path returns None"""
        node = HierarchyNode(path="system")
        value = node.get_value_by_path("nonexistent.path")
        assert value is None

    def test_get_value_by_path_empty_path(self):
        """Test getting value with empty path returns node's own value"""
        node = HierarchyNode(path="system.name", value="MyApp")
        value = node.get_value_by_path("")
        assert value == "MyApp"

    def test_get_node_by_path(self):
        """Test getting node by path"""
        root = HierarchyNode(path="")
        system = HierarchyNode(path="system")
        name = HierarchyNode(path="system.name", value="MyApp")

        root.add_child("system", system)
        system.add_child("name", name)

        retrieved_node = root.get_node_by_path("system.name")
        assert retrieved_node == name

    def test_get_node_by_path_not_found(self):
        """Test getting node by non-existent path returns None"""
        node = HierarchyNode(path="system")
        retrieved = node.get_node_by_path("nonexistent")
        assert retrieved is None

    def test_find_all_by_pattern_single_wildcard(self):
        """Test finding nodes with single wildcard pattern"""
        root = HierarchyNode(path="")
        agents = HierarchyNode(path="agents")

        discovery = HierarchyNode(path="agents.discovery")
        discovery.add_child("model", HierarchyNode(path="agents.discovery.model", value="model1"))

        coder = HierarchyNode(path="agents.coder")
        coder.add_child("model", HierarchyNode(path="agents.coder.model", value="model2"))

        agents.add_child("discovery", discovery)
        agents.add_child("coder", coder)
        root.add_child("agents", agents)

        results = root.find_all_by_pattern("agents.*")
        assert len(results) == 2
        paths = [path for path, _ in results]
        # Pattern matching returns the matched portion of the path
        assert "agents.discovery" in paths or "discovery" in paths
        assert "agents.coder" in paths or "coder" in paths

    def test_find_all_by_pattern_nested_wildcard(self):
        """Test finding nodes with nested wildcard pattern"""
        root = HierarchyNode(path="")
        agents = HierarchyNode(path="agents")

        discovery = HierarchyNode(path="agents.discovery")
        discovery.add_child("model", HierarchyNode(path="agents.discovery.model", value="model1"))

        coder = HierarchyNode(path="agents.coder")
        coder.add_child("model", HierarchyNode(path="agents.coder.model", value="model2"))

        agents.add_child("discovery", discovery)
        agents.add_child("coder", coder)
        root.add_child("agents", agents)

        results = root.find_all_by_pattern("agents.*.model")
        assert len(results) == 2
        values = [node.value for _, node in results]
        assert "model1" in values
        assert "model2" in values

    def test_find_all_by_pattern_exact_match(self):
        """Test finding nodes with exact match (no wildcard)"""
        root = HierarchyNode(path="")
        system = HierarchyNode(path="system")
        name = HierarchyNode(path="system.name", value="MyApp")

        root.add_child("system", system)
        system.add_child("name", name)

        results = root.find_all_by_pattern("system.name")
        assert len(results) == 1
        # Pattern matching returns the matched portion
        assert results[0][0] in ["name", "system.name"]
        assert results[0][1].value == "MyApp"

    def test_to_dict_leaf_with_primitive_value(self):
        """Test converting leaf node with primitive value to dict"""
        node = HierarchyNode(path="system.name", value="MyApp")
        result = node.to_dict()
        assert result == "MyApp"

    def test_to_dict_leaf_with_uri_reference(self):
        """Test converting leaf node with URI reference to dict"""
        uri_ref = URIReference.from_string("file:///test.md")
        node = HierarchyNode(path="prompt", value=uri_ref)
        result = node.to_dict()
        assert result == {
            "_uri": "file:///test.md",
            "_type": "uri_reference"
        }

    def test_to_dict_container(self):
        """Test converting container node to dict"""
        root = HierarchyNode(path="system")
        root.add_child("name", HierarchyNode(path="system.name", value="MyApp"))
        root.add_child("version", HierarchyNode(path="system.version", value="1.0"))

        result = root.to_dict()
        assert result == {
            "name": "MyApp",
            "version": "1.0"
        }

    def test_to_dict_nested_structure(self):
        """Test converting nested structure to dict"""
        root = HierarchyNode(path="")
        system = HierarchyNode(path="system")
        system.add_child("name", HierarchyNode(path="system.name", value="MyApp"))
        system.add_child("version", HierarchyNode(path="system.version", value="1.0"))
        root.add_child("system", system)

        result = root.to_dict()
        assert result == {
            "system": {
                "name": "MyApp",
                "version": "1.0"
            }
        }

    def test_node_repr(self):
        """Test string representation of HierarchyNode"""
        leaf = HierarchyNode(path="system.name", value="MyApp")
        assert "value=" in repr(leaf)
        assert "system.name" in repr(leaf)

        container = HierarchyNode(path="system")
        container.add_child("name", leaf)
        assert "children=" in repr(container)

    def test_is_uri_reference_true(self):
        """Test is_uri_reference returns True for URI reference value"""
        uri_ref = URIReference.from_string("file:///test.md")
        node = HierarchyNode(path="prompt", value=uri_ref)
        assert node.is_uri_reference() is True

    def test_is_uri_reference_false(self):
        """Test is_uri_reference returns False for non-URI value"""
        node = HierarchyNode(path="name", value="test")
        assert node.is_uri_reference() is False

    def test_is_container_true(self):
        """Test is_container returns True for node with children"""
        parent = HierarchyNode(path="system")
        child = HierarchyNode(path="system.name", value="MyApp")
        parent.add_child("name", child)
        assert parent.is_container() is True

    def test_is_container_false(self):
        """Test is_container returns False for node without children"""
        node = HierarchyNode(path="name", value="MyApp")
        assert node.is_container() is False

    def test_is_leaf_true(self):
        """Test is_leaf returns True for leaf node"""
        node = HierarchyNode(path="name", value="MyApp")
        assert node.is_leaf() is True

    def test_is_leaf_false_container(self):
        """Test is_leaf returns False for container node"""
        parent = HierarchyNode(path="system")
        child = HierarchyNode(path="system.name", value="MyApp")
        parent.add_child("name", child)
        assert parent.is_leaf() is False

    def test_is_leaf_false_no_value(self):
        """Test is_leaf returns False for node without value"""
        node = HierarchyNode(path="system")
        assert node.is_leaf() is False

    def test_node_with_various_value_types(self):
        """Test node can hold different value types"""
        # String
        node_str = HierarchyNode(path="str", value="test")
        assert node_str.value == "test"

        # Integer
        node_int = HierarchyNode(path="int", value=42)
        assert node_int.value == 42

        # Float
        node_float = HierarchyNode(path="float", value=3.14)
        assert node_float.value == 3.14

        # Boolean
        node_bool = HierarchyNode(path="bool", value=True)
        assert node_bool.value is True

        # None
        node_none = HierarchyNode(path="none", value=None)
        assert node_none.value is None

        # List
        node_list = HierarchyNode(path="list", value=[1, 2, 3])
        assert node_list.value == [1, 2, 3]

        # Dict
        node_dict = HierarchyNode(path="dict", value={"key": "value"})
        assert node_dict.value == {"key": "value"}
