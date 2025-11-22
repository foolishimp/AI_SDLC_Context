"""
Unit tests for config_manager module.

# Validates: REQ-NFR-FEDERATE-001 (Hierarchical configuration composition)
# Validates: REQ-F-TESTING-001 (Test coverage validation)

Tests cover:
- ConfigManager initialization
- Loading hierarchies from files and strings
- Adding runtime overrides
- Merging configurations
- Accessing values (get_value, get_uri, get_content)
- Finding nodes by pattern
- Registering custom URI resolvers
- Integration with all components
"""
import pytest
import tempfile
from pathlib import Path

from ai_sdlc_config.core.config_manager import ConfigManager
from ai_sdlc_config.mergers.hierarchy_merger import MergeStrategy
from ai_sdlc_config.models.hierarchy_node import URIReference, URIScheme


class TestConfigManager:
    """Test ConfigManager class"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def manager(self, temp_dir):
        """Create a ConfigManager with temporary base path"""
        return ConfigManager(base_path=temp_dir)

    @pytest.fixture
    def sample_yaml_file(self, temp_dir):
        """Create a sample YAML configuration file"""
        yaml_content = """
system:
  name: TestApp
  version: 1.0
  environment: development

llm:
  default_provider: anthropic
  agents:
    discovery:
      model: claude-3-5-sonnet
      temperature: 0.7
    coder:
      model: claude-3-5-sonnet
      temperature: 0.5
"""
        yaml_file = temp_dir / "config.yml"
        yaml_file.write_text(yaml_content)
        return yaml_file

    @pytest.fixture
    def override_yaml_file(self, temp_dir):
        """Create an override YAML configuration file"""
        yaml_content = """
system:
  environment: production
  debug: false

llm:
  agents:
    discovery:
      model: claude-3-7-sonnet
"""
        yaml_file = temp_dir / "override.yml"
        yaml_file.write_text(yaml_content)
        return yaml_file

    def test_create_manager_default_base_path(self):
        """Test creating manager with default base path"""
        manager = ConfigManager()
        assert manager.base_path == Path.cwd()
        assert manager.hierarchies == []
        assert manager.merged_hierarchy is None

    def test_create_manager_custom_base_path(self, temp_dir):
        """Test creating manager with custom base path"""
        manager = ConfigManager(base_path=temp_dir)
        assert manager.base_path == temp_dir

    def test_create_manager_custom_merge_strategy(self, temp_dir):
        """Test creating manager with custom merge strategy"""
        manager = ConfigManager(
            base_path=temp_dir,
            merge_strategy=MergeStrategy.PRESERVE
        )
        assert manager.merger.strategy == MergeStrategy.PRESERVE

    def test_load_hierarchy_absolute_path(self, manager, sample_yaml_file):
        """Test loading hierarchy from absolute path"""
        manager.load_hierarchy(str(sample_yaml_file))
        assert len(manager.hierarchies) == 1
        assert manager.merged_hierarchy is None  # Not yet merged

    def test_load_hierarchy_relative_path(self, temp_dir, sample_yaml_file):
        """Test loading hierarchy from relative path"""
        manager = ConfigManager(base_path=temp_dir)
        manager.load_hierarchy("config.yml")
        assert len(manager.hierarchies) == 1

    def test_load_hierarchy_with_custom_source_name(self, manager, sample_yaml_file):
        """Test loading hierarchy with custom source name"""
        manager.load_hierarchy(str(sample_yaml_file), source_name="custom_source")
        assert len(manager.hierarchies) == 1
        hierarchy = manager.hierarchies[0]
        assert hierarchy.source == "custom_source"

    def test_load_hierarchy_file_not_found(self, manager):
        """Test loading non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            manager.load_hierarchy("nonexistent.yml")

    def test_load_hierarchy_clears_merged_hierarchy(self, manager, sample_yaml_file):
        """Test that loading new hierarchy clears merged hierarchy"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()
        assert manager.merged_hierarchy is not None

        # Load another hierarchy
        manager.load_hierarchy(str(sample_yaml_file))
        assert manager.merged_hierarchy is None

    def test_load_hierarchy_from_string(self, manager):
        """Test loading hierarchy from YAML string"""
        yaml_string = """
system:
  name: StringApp
  version: 2.0
"""
        manager.load_hierarchy_from_string(yaml_string, source_name="string_source")
        assert len(manager.hierarchies) == 1

        manager.merge()
        assert manager.get_value("system.name") == "StringApp"

    def test_add_runtime_overrides(self, manager, sample_yaml_file):
        """Test adding runtime overrides"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.add_runtime_overrides({
            "system.name": "RuntimeApp",
            "system.new_key": "new_value"
        })

        assert len(manager.hierarchies) == 2  # Base + runtime
        runtime_hierarchy = manager.hierarchies[1]
        assert runtime_hierarchy.source == "runtime_overrides"

    def test_add_runtime_overrides_clears_merged(self, manager, sample_yaml_file):
        """Test that adding runtime overrides clears merged hierarchy"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()
        assert manager.merged_hierarchy is not None

        manager.add_runtime_overrides({"system.debug": True})
        assert manager.merged_hierarchy is None

    def test_merge_no_hierarchies_raises_error(self, manager):
        """Test merging with no hierarchies loaded raises ValueError"""
        with pytest.raises(ValueError, match="No hierarchies loaded"):
            manager.merge()

    def test_merge_single_hierarchy(self, manager, sample_yaml_file):
        """Test merging single hierarchy"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        assert manager.merged_hierarchy is not None
        assert manager.get_value("system.name") == "TestApp"

    def test_merge_multiple_hierarchies(
        self,
        manager,
        sample_yaml_file,
        override_yaml_file
    ):
        """Test merging multiple hierarchies with override precedence"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.load_hierarchy(str(override_yaml_file))
        manager.merge()

        # Override values
        assert manager.get_value("system.environment") == "production"
        assert manager.get_value("llm.agents.discovery.model") == "claude-3-7-sonnet"

        # Base values that weren't overridden
        assert manager.get_value("system.name") == "TestApp"
        assert manager.get_value("llm.agents.coder.model") == "claude-3-5-sonnet"

        # Override-only values
        assert manager.get_value("system.debug") is False

    def test_merge_with_runtime_overrides(self, manager, sample_yaml_file):
        """Test merging with runtime overrides has highest priority"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.add_runtime_overrides({
            "system.name": "RuntimeApp"
        })
        manager.merge()

        assert manager.get_value("system.name") == "RuntimeApp"

    def test_get_value_before_merge_raises_error(self, manager, sample_yaml_file):
        """Test getting value before merge raises ValueError"""
        manager.load_hierarchy(str(sample_yaml_file))
        with pytest.raises(ValueError, match="Hierarchy not merged"):
            manager.get_value("system.name")

    def test_get_value_simple_path(self, manager, sample_yaml_file):
        """Test getting value at simple path"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        assert manager.get_value("system.name") == "TestApp"
        assert manager.get_value("system.version") == 1.0

    def test_get_value_nested_path(self, manager, sample_yaml_file):
        """Test getting value at nested path"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        assert manager.get_value("llm.agents.discovery.model") == "claude-3-5-sonnet"
        assert manager.get_value("llm.agents.discovery.temperature") == 0.7

    def test_get_value_nonexistent_path(self, manager, sample_yaml_file):
        """Test getting value at non-existent path returns None"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        assert manager.get_value("nonexistent.path") is None

    def test_get_uri_with_uri_reference(self, manager, temp_dir):
        """Test getting URI string from URI reference"""
        yaml_content = """
prompt: "file:///prompts/test.md"
"""
        yaml_file = temp_dir / "config.yml"
        yaml_file.write_text(yaml_content)

        manager.load_hierarchy(str(yaml_file))
        manager.merge()

        uri = manager.get_uri("prompt")
        assert uri == "file:///prompts/test.md"

    def test_get_uri_with_regular_value(self, manager, sample_yaml_file):
        """Test getting URI from non-URI value returns None"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        uri = manager.get_uri("system.name")
        assert uri is None

    def test_get_content_with_string_value(self, manager, sample_yaml_file):
        """Test getting content from regular string value"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        content = manager.get_content("system.name")
        assert content == "TestApp"

    def test_get_content_with_uri_reference(self, manager, temp_dir):
        """Test getting content resolves URI reference"""
        # Create referenced file
        prompt_file = temp_dir / "prompt.txt"
        prompt_file.write_text("This is the prompt content")

        yaml_content = f"""
prompt: "file://{prompt_file}"
"""
        yaml_file = temp_dir / "config.yml"
        yaml_file.write_text(yaml_content)

        manager.load_hierarchy(str(yaml_file))
        manager.merge()

        content = manager.get_content("prompt")
        assert content == "This is the prompt content"

    def test_get_content_nonexistent_path(self, manager, sample_yaml_file):
        """Test getting content at non-existent path returns None"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        content = manager.get_content("nonexistent.path")
        assert content is None

    def test_get_content_with_numeric_value(self, manager, sample_yaml_file):
        """Test getting content converts numeric values to string"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        content = manager.get_content("system.version")
        assert content == "1.0"

    def test_get_node(self, manager, sample_yaml_file):
        """Test getting node at path"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        node = manager.get_node("system")
        assert node is not None
        assert node.is_container()
        assert "name" in node.children

    def test_get_node_nonexistent_path(self, manager, sample_yaml_file):
        """Test getting node at non-existent path returns None"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        node = manager.get_node("nonexistent")
        assert node is None

    def test_get_node_before_merge_raises_error(self, manager, sample_yaml_file):
        """Test getting node before merge raises ValueError"""
        manager.load_hierarchy(str(sample_yaml_file))
        with pytest.raises(ValueError, match="Hierarchy not merged"):
            manager.get_node("system")

    def test_find_all_with_wildcard(self, manager, sample_yaml_file):
        """Test finding all nodes matching wildcard pattern"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        agents = manager.find_all("llm.agents.*")
        assert len(agents) == 2

        agent_names = [path for path, _ in agents]
        # find_all returns paths that may include the full pattern match
        assert any("discovery" in name for name in agent_names)
        assert any("coder" in name for name in agent_names)

    def test_find_all_nested_wildcard(self, manager, sample_yaml_file):
        """Test finding nodes with nested wildcard pattern"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        models = manager.find_all("llm.agents.*.model")
        assert len(models) == 2

        for _, node in models:
            assert node.value == "claude-3-5-sonnet"

    def test_find_all_before_merge_raises_error(self, manager, sample_yaml_file):
        """Test finding nodes before merge raises ValueError"""
        manager.load_hierarchy(str(sample_yaml_file))
        with pytest.raises(ValueError, match="Hierarchy not merged"):
            manager.find_all("llm.agents.*")

    def test_to_dict(self, manager, sample_yaml_file):
        """Test converting merged hierarchy to dictionary"""
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()

        result = manager.to_dict()
        assert isinstance(result, dict)
        assert "system" in result
        assert result["system"]["name"] == "TestApp"
        assert "llm" in result

    def test_to_dict_before_merge_raises_error(self, manager, sample_yaml_file):
        """Test to_dict before merge raises ValueError"""
        manager.load_hierarchy(str(sample_yaml_file))
        with pytest.raises(ValueError, match="Hierarchy not merged"):
            manager.to_dict()

    def test_register_uri_resolver(self, manager):
        """Test registering custom URI resolver"""
        def custom_resolver(uri_ref):
            return f"Custom content from {uri_ref.uri}"

        manager.register_uri_resolver("custom", custom_resolver)
        assert "custom" in manager.resolver.custom_resolvers

    def test_multiple_load_and_merge_cycles(self, manager, sample_yaml_file):
        """Test loading and merging multiple times"""
        # First cycle
        manager.load_hierarchy(str(sample_yaml_file))
        manager.merge()
        value1 = manager.get_value("system.name")

        # Second cycle - load more and re-merge
        manager.load_hierarchy(str(sample_yaml_file))
        manager.add_runtime_overrides({"system.name": "NewApp"})
        manager.merge()
        value2 = manager.get_value("system.name")

        assert value1 == "TestApp"
        assert value2 == "NewApp"

    def test_add_path_to_hierarchy_helper(self, manager):
        """Test _add_path_to_hierarchy helper method"""
        from ai_sdlc_config.models.hierarchy_node import HierarchyNode

        root = HierarchyNode(path="", source="test")
        manager._add_path_to_hierarchy(root, "a.b.c.value", "test_value")

        assert root.get_value_by_path("a.b.c.value") == "test_value"
        a_node = root.get_node_by_path("a")
        assert a_node.source == "runtime_overrides"

    def test_complex_integration_scenario(self, temp_dir):
        """Test complex integration scenario with multiple layers"""
        # Create base config
        base_yaml = """
system:
  name: BaseApp
  version: 1.0

agents:
  discovery:
    model: base-model
    temperature: 0.7
  coder:
    model: base-model
    temperature: 0.5
"""
        base_file = temp_dir / "base.yml"
        base_file.write_text(base_yaml)

        # Create dev config
        dev_yaml = """
system:
  environment: development
  debug: true

agents:
  discovery:
    model: dev-model
"""
        dev_file = temp_dir / "dev.yml"
        dev_file.write_text(dev_yaml)

        # Create prod config
        prod_yaml = """
system:
  environment: production
  debug: false

agents:
  discovery:
    model: prod-model
    temperature: 0.3
"""
        prod_file = temp_dir / "prod.yml"
        prod_file.write_text(prod_yaml)

        # Test dev environment
        manager_dev = ConfigManager(base_path=temp_dir)
        manager_dev.load_hierarchy("base.yml")
        manager_dev.load_hierarchy("dev.yml")
        manager_dev.merge()

        assert manager_dev.get_value("system.environment") == "development"
        assert manager_dev.get_value("agents.discovery.model") == "dev-model"
        assert manager_dev.get_value("agents.discovery.temperature") == 0.7
        assert manager_dev.get_value("agents.coder.model") == "base-model"

        # Test prod environment
        manager_prod = ConfigManager(base_path=temp_dir)
        manager_prod.load_hierarchy("base.yml")
        manager_prod.load_hierarchy("prod.yml")
        manager_prod.add_runtime_overrides({
            "system.session_id": "prod-12345"
        })
        manager_prod.merge()

        assert manager_prod.get_value("system.environment") == "production"
        assert manager_prod.get_value("agents.discovery.model") == "prod-model"
        assert manager_prod.get_value("agents.discovery.temperature") == 0.3
        assert manager_prod.get_value("system.session_id") == "prod-12345"

    def test_uri_reference_with_metadata(self, manager, temp_dir):
        """Test loading and accessing URI reference with metadata"""
        yaml_content = """
prompt:
  uri: "file:///test.md"
  content_type: "text/markdown"
  version: "1.0"
"""
        yaml_file = temp_dir / "config.yml"
        yaml_file.write_text(yaml_content)

        manager.load_hierarchy(str(yaml_file))
        manager.merge()

        value = manager.get_value("prompt")
        assert isinstance(value, URIReference)
        assert value.content_type == "text/markdown"
        assert value.metadata["version"] == "1.0"

    def test_loading_yaml_with_lists(self, manager, temp_dir):
        """Test loading YAML with list values"""
        yaml_content = """
items:
  - name: item1
    value: 10
  - name: item2
    value: 20
"""
        yaml_file = temp_dir / "config.yml"
        yaml_file.write_text(yaml_content)

        manager.load_hierarchy(str(yaml_file))
        manager.merge()

        # Lists are converted to children with numeric keys
        item0 = manager.get_value("items.0.name")
        item1 = manager.get_value("items.1.name")
        assert item0 == "item1"
        assert item1 == "item2"

    def test_error_handling_chain(self, manager):
        """Test that errors propagate correctly through the chain"""
        # Test file not found
        with pytest.raises(FileNotFoundError):
            manager.load_hierarchy("nonexistent.yml")

        # Test merge before load
        with pytest.raises(ValueError):
            manager.merge()

        # Test get before merge
        manager.load_hierarchy_from_string("key: value", "test")
        with pytest.raises(ValueError):
            manager.get_value("key")
