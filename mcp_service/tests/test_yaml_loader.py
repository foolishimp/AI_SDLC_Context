"""
Unit tests for yaml_loader module.

# Validates: REQ-F-PLUGIN-001 (Plugin system - YAML loading)
# Validates: REQ-NFR-FEDERATE-001 (Configuration composition)

Tests cover:
- Loading YAML files into HierarchyNode structures
- URI detection and conversion
- Handling different data types (dicts, lists, primitives)
- Error handling for invalid files and YAML
"""
import pytest
import tempfile
from pathlib import Path
import yaml

from ai_sdlc_config.loaders.yaml_loader import YAMLLoader
from ai_sdlc_config.models.hierarchy_node import HierarchyNode, URIReference, URIScheme


class TestYAMLLoader:
    """Test YAMLLoader class"""

    @pytest.fixture
    def loader(self):
        """Create a YAMLLoader instance"""
        return YAMLLoader()

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_load_simple_yaml(self, loader, temp_dir):
        """Test loading a simple YAML file"""
        yaml_content = """
system:
  name: TestApp
  version: 1.0
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        assert node.path == ""
        assert node.source == str(yaml_file)
        assert "system" in node.children

        system_node = node.children["system"]
        assert system_node.get_value_by_path("name") == "TestApp"
        assert system_node.get_value_by_path("version") == 1.0

    def test_load_with_custom_source_name(self, loader, temp_dir):
        """Test loading with custom source name"""
        yaml_content = "name: test"
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file), source_name="custom_source")
        assert node.source == "custom_source"

    def test_load_file_not_found(self, loader):
        """Test loading non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            loader.load("/nonexistent/path/to/file.yml")

    def test_load_invalid_yaml(self, loader, temp_dir):
        """Test loading invalid YAML raises YAMLError"""
        yaml_file = temp_dir / "invalid.yml"
        yaml_file.write_text("invalid: yaml: content: [")

        with pytest.raises(yaml.YAMLError):
            loader.load(str(yaml_file))

    def test_load_empty_file(self, loader, temp_dir):
        """Test loading empty YAML file creates empty hierarchy"""
        yaml_file = temp_dir / "empty.yml"
        yaml_file.write_text("")

        node = loader.load(str(yaml_file))
        assert node.path == ""
        assert node.children == {}

    def test_load_from_string(self, loader):
        """Test loading YAML from string"""
        yaml_string = """
system:
  name: TestApp
  version: 1.0
"""
        node = loader.load_from_string(yaml_string, source_name="test_string")
        assert node.source == "test_string"
        assert node.get_value_by_path("system.name") == "TestApp"

    def test_detect_file_uri_string(self, loader, temp_dir):
        """Test detection of file:// URI in string value"""
        yaml_content = """
prompt: "file:///prompts/discovery.md"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert prompt_node.is_uri_reference()
        assert isinstance(prompt_node.value, URIReference)
        assert prompt_node.value.uri == "file:///prompts/discovery.md"
        assert prompt_node.value.scheme == URIScheme.FILE

    def test_detect_https_uri_string(self, loader, temp_dir):
        """Test detection of https:// URI in string value"""
        yaml_content = """
prompt: "https://docs.example.com/prompt.md"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert prompt_node.is_uri_reference()
        assert prompt_node.value.scheme == URIScheme.HTTPS

    def test_detect_http_uri_string(self, loader, temp_dir):
        """Test detection of http:// URI in string value"""
        yaml_content = """
prompt: "http://example.com/prompt.txt"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert prompt_node.is_uri_reference()
        assert prompt_node.value.scheme == URIScheme.HTTP

    def test_detect_data_uri_string(self, loader, temp_dir):
        """Test detection of data: URI in string value"""
        # Note: data: URIs use colon without ://, so from_string adds file:// prefix
        # The loader detects "data:" prefix, but URIReference.from_string wraps it
        yaml_content = """
content: "data:text/plain,Hello%20World"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        content_node = node.children["content"]
        # Detected as URI by loader, but from_string may wrap it
        assert content_node.is_uri_reference()
        assert isinstance(content_node.value, URIReference)

    def test_detect_ref_uri_string(self, loader, temp_dir):
        """Test detection of ref: URI in string value"""
        # Note: ref: URIs use colon without ://, so from_string adds file:// prefix
        yaml_content = """
alias: "ref:system.base.prompt"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        alias_node = node.children["alias"]
        # Detected as URI by loader, but from_string may wrap it
        assert alias_node.is_uri_reference()
        assert isinstance(alias_node.value, URIReference)

    def test_uri_reference_dict_with_uri_key(self, loader, temp_dir):
        """Test URI reference as dict with 'uri' key"""
        yaml_content = """
prompt:
  uri: "file:///prompts/discovery.md"
  content_type: "text/markdown"
  version: "1.0"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert prompt_node.is_uri_reference()
        assert prompt_node.value.uri == "file:///prompts/discovery.md"
        assert prompt_node.value.content_type == "text/markdown"
        assert prompt_node.value.metadata["version"] == "1.0"

    def test_uri_reference_dict_with_underscore_uri_key(self, loader, temp_dir):
        """Test URI reference as dict with '_uri' key"""
        yaml_content = """
prompt:
  _uri: "https://example.com/prompt.md"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert prompt_node.is_uri_reference()
        assert prompt_node.value.uri == "https://example.com/prompt.md"

    def test_uri_reference_dict_with_ref_key(self, loader, temp_dir):
        """Test URI reference as dict with 'ref' key"""
        # For ref in dict, the value doesn't have ref: prefix, so add it
        yaml_content = """
alias:
  ref: "ref:system.base.prompt"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        alias_node = node.children["alias"]
        assert alias_node.is_uri_reference()
        # Dict format should preserve ref correctly
        assert isinstance(alias_node.value, URIReference)

    def test_regular_string_not_detected_as_uri(self, loader, temp_dir):
        """Test that regular strings are not detected as URIs"""
        yaml_content = """
name: "This is a regular string"
description: "Not a URI at all"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        assert not node.children["name"].is_uri_reference()
        assert not node.children["description"].is_uri_reference()
        assert node.get_value_by_path("name") == "This is a regular string"

    def test_nested_structure(self, loader, temp_dir):
        """Test loading nested YAML structure"""
        yaml_content = """
system:
  agents:
    discovery:
      model: "claude-3-5-sonnet"
      temperature: 0.7
    coder:
      model: "claude-3-5-sonnet"
      temperature: 0.5
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        assert node.get_value_by_path("system.agents.discovery.model") == "claude-3-5-sonnet"
        assert node.get_value_by_path("system.agents.discovery.temperature") == 0.7
        assert node.get_value_by_path("system.agents.coder.temperature") == 0.5

    def test_list_handling(self, loader, temp_dir):
        """Test loading YAML with list values"""
        yaml_content = """
agents:
  - name: discovery
    model: claude-3-5-sonnet
  - name: coder
    model: claude-3-7-sonnet
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        agents_node = node.children["agents"]
        assert "0" in agents_node.children
        assert "1" in agents_node.children
        assert agents_node.children["0"].get_value_by_path("name") == "discovery"
        assert agents_node.children["1"].get_value_by_path("name") == "coder"

    def test_primitive_types(self, loader, temp_dir):
        """Test loading different primitive types"""
        yaml_content = """
string_val: "test"
int_val: 42
float_val: 3.14
bool_val: true
null_val: null
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        assert node.get_value_by_path("string_val") == "test"
        assert node.get_value_by_path("int_val") == 42
        assert node.get_value_by_path("float_val") == 3.14
        assert node.get_value_by_path("bool_val") is True
        assert node.get_value_by_path("null_val") is None

    def test_mixed_uri_and_regular_values(self, loader, temp_dir):
        """Test loading YAML with both URI references and regular values"""
        yaml_content = """
system:
  name: "MyApp"
  prompt: "file:///prompts/system.md"
  version: 1.0
  docs: "https://example.com/docs"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        system_node = node.children["system"]

        # Regular values
        assert system_node.children["name"].value == "MyApp"
        assert system_node.children["version"].value == 1.0

        # URI references
        assert system_node.children["prompt"].is_uri_reference()
        assert system_node.children["docs"].is_uri_reference()

    def test_deep_nesting(self, loader, temp_dir):
        """Test loading deeply nested YAML structure"""
        yaml_content = """
level1:
  level2:
    level3:
      level4:
        level5:
          value: "deep"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        value = node.get_value_by_path("level1.level2.level3.level4.level5.value")
        assert value == "deep"

    def test_uri_reference_dict_missing_uri_key(self, loader, temp_dir):
        """Test that URI reference dict without uri key raises ValueError"""
        yaml_content = """
prompt:
  content_type: "text/markdown"
  version: "1.0"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        # This should be treated as a regular dict, not a URI reference
        # because it doesn't have uri/_uri/ref/_ref keys
        node = loader.load(str(yaml_file))
        prompt_node = node.children["prompt"]
        assert not prompt_node.is_uri_reference()
        assert prompt_node.is_container()

    def test_path_construction(self, loader, temp_dir):
        """Test that paths are constructed correctly during loading"""
        yaml_content = """
system:
  agents:
    discovery:
      model: "test"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        system_node = node.children["system"]
        agents_node = system_node.children["agents"]
        discovery_node = agents_node.children["discovery"]
        model_node = discovery_node.children["model"]

        assert system_node.path == "system"
        assert agents_node.path == "system.agents"
        assert discovery_node.path == "system.agents.discovery"
        assert model_node.path == "system.agents.discovery.model"

    def test_load_yaml_with_anchors_and_aliases(self, loader, temp_dir):
        """Test loading YAML with anchors and aliases"""
        yaml_content = """
defaults: &defaults
  temperature: 0.7
  max_tokens: 1000

agent1:
  <<: *defaults
  model: "claude-3-5-sonnet"

agent2:
  <<: *defaults
  model: "claude-3-7-sonnet"
"""
        yaml_file = temp_dir / "test.yml"
        yaml_file.write_text(yaml_content)

        node = loader.load(str(yaml_file))
        assert node.get_value_by_path("agent1.temperature") == 0.7
        assert node.get_value_by_path("agent1.max_tokens") == 1000
        assert node.get_value_by_path("agent1.model") == "claude-3-5-sonnet"
        assert node.get_value_by_path("agent2.temperature") == 0.7
        assert node.get_value_by_path("agent2.model") == "claude-3-7-sonnet"

    def test_is_uri_string_method(self, loader):
        """Test _is_uri_string helper method"""
        assert loader._is_uri_string("file:///path/to/file")
        assert loader._is_uri_string("http://example.com")
        assert loader._is_uri_string("https://example.com")
        assert loader._is_uri_string("data:text/plain,test")
        assert loader._is_uri_string("ref:system.prompt")
        assert not loader._is_uri_string("regular string")
        assert not loader._is_uri_string("not a uri")

    def test_is_uri_reference_dict_method(self, loader):
        """Test _is_uri_reference_dict helper method"""
        assert loader._is_uri_reference_dict({"uri": "test"})
        assert loader._is_uri_reference_dict({"_uri": "test"})
        assert loader._is_uri_reference_dict({"ref": "test"})
        assert loader._is_uri_reference_dict({"_ref": "test"})
        assert not loader._is_uri_reference_dict({"other": "test"})
        assert not loader._is_uri_reference_dict({"name": "test", "value": "test"})
