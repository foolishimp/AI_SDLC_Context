"""
Unit tests for hierarchy_merger module.

# Validates: REQ-NFR-FEDERATE-001 (Hierarchical configuration composition)
# Validates: REQ-F-PLUGIN-002 (Federated plugin loading)

Tests cover:
- MergeStrategy enum
- Basic two-node merging
- Multi-hierarchy merging with priorities
- Override strategies (OVERRIDE, PRESERVE, URI_PRIORITY)
- Merge with runtime overrides
- Conflict resolution
- Nested structure merging
- MergeReport functionality
"""
import pytest
from ai_sdlc_config.mergers.hierarchy_merger import (
    HierarchyMerger,
    MergeStrategy,
    MergeReport
)
from ai_sdlc_config.models.hierarchy_node import (
    HierarchyNode,
    URIReference,
    URIScheme
)


class TestMergeStrategy:
    """Test MergeStrategy enum"""

    def test_all_strategies_exist(self):
        """Verify all expected merge strategies are defined"""
        assert MergeStrategy.OVERRIDE.value == "override"
        assert MergeStrategy.PRESERVE.value == "preserve"
        assert MergeStrategy.URI_PRIORITY.value == "uri_priority"
        assert MergeStrategy.DEEP_MERGE.value == "deep_merge"


class TestHierarchyMerger:
    """Test HierarchyMerger class"""

    @pytest.fixture
    def merger(self):
        """Create a HierarchyMerger with default strategy"""
        return HierarchyMerger(strategy=MergeStrategy.OVERRIDE)

    @pytest.fixture
    def simple_base_hierarchy(self):
        """Create a simple base hierarchy"""
        root = HierarchyNode(path="", source="base.yml")
        system = HierarchyNode(path="system")
        system.add_child("name", HierarchyNode(path="system.name", value="BaseApp"))
        system.add_child("version", HierarchyNode(path="system.version", value="1.0"))
        root.add_child("system", system)
        return root

    @pytest.fixture
    def simple_override_hierarchy(self):
        """Create a simple override hierarchy"""
        root = HierarchyNode(path="", source="override.yml")
        system = HierarchyNode(path="system")
        system.add_child("name", HierarchyNode(path="system.name", value="OverrideApp"))
        system.add_child("environment", HierarchyNode(path="system.environment", value="production"))
        root.add_child("system", system)
        return root

    def test_create_merger_default_strategy(self):
        """Test creating merger with default strategy"""
        merger = HierarchyMerger()
        assert merger.strategy == MergeStrategy.OVERRIDE

    def test_create_merger_custom_strategy(self):
        """Test creating merger with custom strategy"""
        merger = HierarchyMerger(strategy=MergeStrategy.PRESERVE)
        assert merger.strategy == MergeStrategy.PRESERVE

    def test_merge_empty_list_raises_error(self, merger):
        """Test merging empty list raises ValueError"""
        with pytest.raises(ValueError, match="Cannot merge empty list"):
            merger.merge([])

    def test_merge_single_hierarchy(self, merger, simple_base_hierarchy):
        """Test merging single hierarchy returns deep copy"""
        result = merger.merge([simple_base_hierarchy])
        assert result is not simple_base_hierarchy  # Different object
        assert result.get_value_by_path("system.name") == "BaseApp"
        assert result.get_value_by_path("system.version") == "1.0"

    def test_merge_two_hierarchies_override_strategy(
        self,
        merger,
        simple_base_hierarchy,
        simple_override_hierarchy
    ):
        """Test merging two hierarchies with OVERRIDE strategy"""
        result = merger.merge([simple_base_hierarchy, simple_override_hierarchy])

        # Override value should win
        assert result.get_value_by_path("system.name") == "OverrideApp"

        # Base-only value should remain
        assert result.get_value_by_path("system.version") == "1.0"

        # Override-only value should be added
        assert result.get_value_by_path("system.environment") == "production"

    def test_merge_three_hierarchies_priority_order(self, merger):
        """Test merging three hierarchies respects priority order"""
        # Base: lowest priority
        base = HierarchyNode(path="", source="base.yml")
        base.add_child("value", HierarchyNode(path="value", value="base"))

        # Dev: medium priority
        dev = HierarchyNode(path="", source="dev.yml")
        dev.add_child("value", HierarchyNode(path="value", value="dev"))

        # Runtime: highest priority
        runtime = HierarchyNode(path="", source="runtime.yml")
        runtime.add_child("value", HierarchyNode(path="value", value="runtime"))

        result = merger.merge([base, dev, runtime])
        assert result.get_value_by_path("value") == "runtime"

    def test_merge_preserves_priority(self, merger):
        """Test merge tracks priority levels"""
        base = HierarchyNode(path="")
        base.add_child("value", HierarchyNode(path="value", value="base"))

        override = HierarchyNode(path="")
        override.add_child("value", HierarchyNode(path="value", value="override"))

        result = merger.merge([base, override])
        value_node = result.get_node_by_path("value")
        assert value_node.priority == 1  # Priority from second hierarchy

    def test_merge_nested_structures(self, merger):
        """Test merging deeply nested structures"""
        # Base hierarchy
        base = HierarchyNode(path="")
        agents = HierarchyNode(path="agents")
        discovery = HierarchyNode(path="agents.discovery")
        discovery.add_child("model", HierarchyNode(path="agents.discovery.model", value="base-model"))
        discovery.add_child("temp", HierarchyNode(path="agents.discovery.temp", value=0.7))
        agents.add_child("discovery", discovery)
        base.add_child("agents", agents)

        # Override hierarchy (changes model, adds max_tokens)
        override = HierarchyNode(path="")
        agents_o = HierarchyNode(path="agents")
        discovery_o = HierarchyNode(path="agents.discovery")
        discovery_o.add_child("model", HierarchyNode(path="agents.discovery.model", value="override-model"))
        discovery_o.add_child("max_tokens", HierarchyNode(path="agents.discovery.max_tokens", value=1000))
        agents_o.add_child("discovery", discovery_o)
        override.add_child("agents", agents_o)

        result = merger.merge([base, override])

        # Check merged values
        assert result.get_value_by_path("agents.discovery.model") == "override-model"
        assert result.get_value_by_path("agents.discovery.temp") == 0.7
        assert result.get_value_by_path("agents.discovery.max_tokens") == 1000

    def test_merge_with_uri_references(self, merger):
        """Test merging hierarchies containing URI references"""
        # Base with regular value
        base = HierarchyNode(path="")
        base.add_child("prompt", HierarchyNode(path="prompt", value="inline prompt"))

        # Override with URI reference
        override = HierarchyNode(path="")
        uri_ref = URIReference(uri="file:///prompts/test.md", scheme=URIScheme.FILE)
        override.add_child("prompt", HierarchyNode(path="prompt", value=uri_ref))

        result = merger.merge([base, override])
        prompt_node = result.get_node_by_path("prompt")
        assert prompt_node.is_uri_reference()
        assert prompt_node.value.uri == "file:///prompts/test.md"

    def test_merge_uri_priority_strategy(self):
        """Test merging with URI_PRIORITY strategy"""
        merger = HierarchyMerger(strategy=MergeStrategy.URI_PRIORITY)

        # Base with URI
        base = HierarchyNode(path="")
        uri_ref = URIReference(uri="file:///base.md", scheme=URIScheme.FILE)
        base.add_child("prompt", HierarchyNode(path="prompt", value=uri_ref))

        # Override with regular value
        override = HierarchyNode(path="")
        override.add_child("prompt", HierarchyNode(path="prompt", value="regular text"))

        result = merger.merge([base, override])

        # With URI_PRIORITY strategy:
        # - If override has URI, override wins
        # - If override doesn't have URI but base does, depends on strategy implementation
        # Looking at the code, when override doesn't have URI but base does, base URI is kept
        prompt_node = result.get_node_by_path("prompt")
        # Base has URI, override doesn't -> base URI should be preserved
        assert isinstance(prompt_node.value, URIReference)
        assert prompt_node.value.uri == "file:///base.md"

    def test_merge_uri_priority_both_have_uri(self):
        """Test URI_PRIORITY when both hierarchies have URIs"""
        merger = HierarchyMerger(strategy=MergeStrategy.URI_PRIORITY)

        # Base with URI
        base = HierarchyNode(path="")
        base_uri = URIReference(uri="file:///base.md", scheme=URIScheme.FILE)
        base.add_child("prompt", HierarchyNode(path="prompt", value=base_uri))

        # Override with URI
        override = HierarchyNode(path="")
        override_uri = URIReference(uri="file:///override.md", scheme=URIScheme.FILE)
        override.add_child("prompt", HierarchyNode(path="prompt", value=override_uri))

        result = merger.merge([base, override])

        # Override URI should win
        prompt_node = result.get_node_by_path("prompt")
        assert prompt_node.value.uri == "file:///override.md"

    def test_merge_with_runtime_overrides(self, merger, simple_base_hierarchy):
        """Test merge_with_overrides method"""
        overrides = {
            "system.name": "RuntimeApp",
            "system.new_key": "new_value"
        }

        result = merger.merge_with_overrides(simple_base_hierarchy, overrides)

        assert result.get_value_by_path("system.name") == "RuntimeApp"
        assert result.get_value_by_path("system.version") == "1.0"
        assert result.get_value_by_path("system.new_key") == "new_value"

    def test_merge_with_overrides_creates_missing_paths(self, merger):
        """Test that merge_with_overrides creates missing intermediate nodes"""
        base = HierarchyNode(path="")
        overrides = {
            "deep.nested.path.value": "test"
        }

        result = merger.merge_with_overrides(base, overrides)
        assert result.get_value_by_path("deep.nested.path.value") == "test"

    def test_merge_with_overrides_uri_reference(self, merger, simple_base_hierarchy):
        """Test merge_with_overrides with URI reference value"""
        uri_ref = URIReference(uri="file:///test.md", scheme=URIScheme.FILE)
        overrides = {
            "system.prompt": uri_ref
        }

        result = merger.merge_with_overrides(simple_base_hierarchy, overrides)
        prompt_node = result.get_node_by_path("system.prompt")
        assert prompt_node.is_uri_reference()

    def test_merge_container_over_leaf(self, merger):
        """Test merging where override changes leaf to container"""
        # Base: leaf node
        base = HierarchyNode(path="")
        base.add_child("config", HierarchyNode(path="config", value="simple value"))

        # Override: container node
        override = HierarchyNode(path="")
        config = HierarchyNode(path="config")
        config.add_child("key1", HierarchyNode(path="config.key1", value="value1"))
        config.add_child("key2", HierarchyNode(path="config.key2", value="value2"))
        override.add_child("config", config)

        result = merger.merge([base, override])

        # Override should transform leaf to container
        config_node = result.get_node_by_path("config")
        assert config_node.is_container()
        assert result.get_value_by_path("config.key1") == "value1"
        assert result.get_value_by_path("config.key2") == "value2"

    def test_merge_leaf_over_container(self, merger):
        """Test merging where override changes container to leaf"""
        # Base: container node
        base = HierarchyNode(path="")
        config = HierarchyNode(path="config")
        config.add_child("key1", HierarchyNode(path="config.key1", value="value1"))
        base.add_child("config", config)

        # Override: leaf node
        override = HierarchyNode(path="")
        override.add_child("config", HierarchyNode(path="config", value="simple value"))

        result = merger.merge([base, override])

        # Override should replace container with leaf
        config_node = result.get_node_by_path("config")
        assert config_node.is_leaf()
        assert config_node.value == "simple value"

    def test_merge_preserves_source_tracking(self, merger):
        """Test that merge preserves source tracking"""
        base = HierarchyNode(path="", source="base.yml")
        base.add_child("from_base", HierarchyNode(path="from_base", value="base", source="base.yml"))

        override = HierarchyNode(path="", source="override.yml")
        override.add_child("from_override", HierarchyNode(path="from_override", value="override", source="override.yml"))

        result = merger.merge([base, override])

        base_node = result.get_node_by_path("from_base")
        override_node = result.get_node_by_path("from_override")

        assert base_node.source == "base.yml"
        assert override_node.source == "override.yml"

    def test_merge_multiple_levels_deep(self, merger):
        """Test merging very deeply nested structures"""
        # Base
        base = HierarchyNode(path="")
        current = base
        for i in range(5):
            child = HierarchyNode(path=f"level{i}")
            current.add_child(f"level{i}", child)
            current = child
        current.add_child("value", HierarchyNode(path="value", value="base"))

        # Override
        override = HierarchyNode(path="")
        current = override
        for i in range(5):
            child = HierarchyNode(path=f"level{i}")
            current.add_child(f"level{i}", child)
            current = child
        current.add_child("value", HierarchyNode(path="value", value="override"))

        result = merger.merge([base, override])
        assert result.get_value_by_path("level0.level1.level2.level3.level4.value") == "override"

    def test_merge_with_multiple_children_at_same_level(self, merger):
        """Test merging nodes with multiple children at the same level"""
        # Base
        base = HierarchyNode(path="")
        agents = HierarchyNode(path="agents")
        agents.add_child("agent1", HierarchyNode(path="agents.agent1", value="base1"))
        agents.add_child("agent2", HierarchyNode(path="agents.agent2", value="base2"))
        agents.add_child("agent3", HierarchyNode(path="agents.agent3", value="base3"))
        base.add_child("agents", agents)

        # Override (changes agent2, adds agent4)
        override = HierarchyNode(path="")
        agents_o = HierarchyNode(path="agents")
        agents_o.add_child("agent2", HierarchyNode(path="agents.agent2", value="override2"))
        agents_o.add_child("agent4", HierarchyNode(path="agents.agent4", value="override4"))
        override.add_child("agents", agents_o)

        result = merger.merge([base, override])

        assert result.get_value_by_path("agents.agent1") == "base1"
        assert result.get_value_by_path("agents.agent2") == "override2"
        assert result.get_value_by_path("agents.agent3") == "base3"
        assert result.get_value_by_path("agents.agent4") == "override4"

    def test_merge_does_not_mutate_originals(self, merger, simple_base_hierarchy, simple_override_hierarchy):
        """Test that merge does not mutate original hierarchies"""
        original_base_name = simple_base_hierarchy.get_value_by_path("system.name")
        original_override_name = simple_override_hierarchy.get_value_by_path("system.name")

        result = merger.merge([simple_base_hierarchy, simple_override_hierarchy])

        # Originals should be unchanged
        assert simple_base_hierarchy.get_value_by_path("system.name") == original_base_name
        assert simple_override_hierarchy.get_value_by_path("system.name") == original_override_name

        # Result should have override value
        assert result.get_value_by_path("system.name") == "OverrideApp"

    def test_set_value_at_path(self, merger):
        """Test _set_value_at_path helper method"""
        root = HierarchyNode(path="")
        merger._set_value_at_path(root, "system.config.value", "test")

        assert root.get_value_by_path("system.config.value") == "test"
        system_node = root.get_node_by_path("system")
        assert system_node.source == "runtime_override"

    def test_merge_with_different_primitive_types(self, merger):
        """Test merging nodes with different primitive value types"""
        # Base with various types
        base = HierarchyNode(path="")
        base.add_child("string", HierarchyNode(path="string", value="text"))
        base.add_child("int", HierarchyNode(path="int", value=42))
        base.add_child("float", HierarchyNode(path="float", value=3.14))
        base.add_child("bool", HierarchyNode(path="bool", value=False))

        # Override changes types
        override = HierarchyNode(path="")
        override.add_child("string", HierarchyNode(path="string", value="new text"))
        override.add_child("int", HierarchyNode(path="int", value=100))
        override.add_child("float", HierarchyNode(path="float", value=2.71))
        override.add_child("bool", HierarchyNode(path="bool", value=True))

        result = merger.merge([base, override])

        assert result.get_value_by_path("string") == "new text"
        assert result.get_value_by_path("int") == 100
        assert result.get_value_by_path("float") == 2.71
        assert result.get_value_by_path("bool") is True


class TestMergeReport:
    """Test MergeReport class"""

    def test_create_merge_report(self):
        """Test creating empty merge report"""
        report = MergeReport()
        assert report.merged_paths == []
        assert report.conflicts == []
        assert report.uri_references == []

    def test_add_merge_to_report(self):
        """Test adding merge operation to report"""
        report = MergeReport()
        report.add_merge("system.name", "base.yml", "override.yml")

        assert len(report.merged_paths) == 1
        assert "system.name" in report.merged_paths
        assert len(report.conflicts) == 1
        assert report.conflicts[0]["path"] == "system.name"
        assert report.conflicts[0]["base_source"] == "base.yml"
        assert report.conflicts[0]["override_source"] == "override.yml"

    def test_add_uri_reference_to_report(self):
        """Test adding URI reference to report"""
        report = MergeReport()
        report.add_uri_reference("system.prompt", "file:///test.md", "config.yml")

        assert len(report.uri_references) == 1
        assert report.uri_references[0]["path"] == "system.prompt"
        assert report.uri_references[0]["uri"] == "file:///test.md"
        assert report.uri_references[0]["source"] == "config.yml"

    def test_report_to_dict(self):
        """Test converting report to dictionary"""
        report = MergeReport()
        report.add_merge("path1", "base", "override")
        report.add_merge("path2", "base", "override")
        report.add_uri_reference("uri_path", "file:///test", "source")

        result = report.to_dict()

        assert result["total_merges"] == 2
        assert len(result["conflicts"]) == 2
        assert len(result["uri_references"]) == 1
