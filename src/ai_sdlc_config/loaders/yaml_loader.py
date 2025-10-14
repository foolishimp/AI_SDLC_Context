"""
YAML configuration loader that builds HierarchyNode structures.

Inspired by C4H's load_config() but builds HierarchyNode trees
and detects URI references.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import yaml

from ..models.hierarchy_node import HierarchyNode, URIReference, NodeValue


class YAMLLoader:
    """
    Loads YAML configuration files into HierarchyNode structures.

    Detects URI references in YAML and converts them to URIReference objects.

    URI Detection:
    1. String value starting with scheme:// → URIReference
    2. Dict with "_uri" or "uri" key → URIReference with metadata
    3. Dict with "_ref" key → Internal reference

    Example YAML:
        system:
          prompts:
            discovery: "file:///prompts/discovery.md"  # Detected as URI
            coder:
              uri: "https://docs.example.com/prompts/coder"
              content_type: "text/markdown"
          agents:
            discovery:
              model: "claude-3-5-sonnet"  # Regular value
    """

    def __init__(self):
        self.uri_schemes = ["file://", "http://", "https://", "data:", "ref:"]

    def load(self, file_path: str, source_name: Optional[str] = None) -> HierarchyNode:
        """
        Load YAML file into HierarchyNode structure.

        Args:
            file_path: Path to YAML file
            source_name: Optional name for tracking source (defaults to file_path)

        Returns:
            Root HierarchyNode

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f) or {}

        source = source_name or str(file_path)
        return self._build_hierarchy(data, path="", source=source)

    def load_from_string(self, yaml_string: str, source_name: str = "string") -> HierarchyNode:
        """
        Load YAML from string into HierarchyNode structure.

        Args:
            yaml_string: YAML content as string
            source_name: Name for tracking source

        Returns:
            Root HierarchyNode
        """
        data = yaml.safe_load(yaml_string) or {}
        return self._build_hierarchy(data, path="", source=source_name)

    def _build_hierarchy(
        self,
        data: Any,
        path: str,
        source: str,
        parent: Optional[HierarchyNode] = None
    ) -> HierarchyNode:
        """
        Recursively build HierarchyNode tree from dictionary.

        Args:
            data: Data to convert (dict, list, or primitive)
            path: Current dot-delimited path
            source: Source file/name
            parent: Parent node (for context)

        Returns:
            HierarchyNode
        """
        node = HierarchyNode(path=path, source=source)

        # Handle dictionary (container with children)
        if isinstance(data, dict):
            # Check if this dict represents a URI reference
            if self._is_uri_reference_dict(data):
                node.value = self._create_uri_reference(data)
            else:
                # Regular dict - create children
                for key, value in data.items():
                    child_path = f"{path}.{key}" if path else key
                    child = self._build_hierarchy(value, child_path, source, node)
                    node.add_child(key, child)

        # Handle list (convert to dict with numeric keys)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                child_path = f"{path}[{i}]"
                child = self._build_hierarchy(item, child_path, source, node)
                node.add_child(str(i), child)

        # Handle string (check if URI)
        elif isinstance(data, str):
            if self._is_uri_string(data):
                node.value = URIReference.from_string(data)
            else:
                node.value = data

        # Handle primitives
        else:
            node.value = data

        return node

    def _is_uri_string(self, value: str) -> bool:
        """Check if string value is a URI"""
        return any(value.startswith(scheme) for scheme in self.uri_schemes)

    def _is_uri_reference_dict(self, data: Dict[str, Any]) -> bool:
        """
        Check if dictionary represents a URI reference.

        URI reference dicts have special keys like "uri", "_uri", or "_ref"
        """
        uri_keys = {"uri", "_uri", "ref", "_ref"}
        return any(key in data for key in uri_keys)

    def _create_uri_reference(self, data: Dict[str, Any]) -> URIReference:
        """
        Create URIReference from dictionary.

        Example dict:
            {
                "uri": "file:///prompts/discovery.md",
                "content_type": "text/markdown",
                "version": "1.0"
            }
        """
        uri_str = data.get("uri") or data.get("_uri") or data.get("ref") or data.get("_ref")
        if not uri_str:
            raise ValueError(f"URI reference dict missing uri key: {data}")

        uri_ref = URIReference.from_string(uri_str)

        # Extract metadata
        if "content_type" in data:
            uri_ref.content_type = data["content_type"]

        # Store other keys as metadata
        metadata_keys = set(data.keys()) - {"uri", "_uri", "ref", "_ref", "content_type"}
        for key in metadata_keys:
            uri_ref.metadata[key] = data[key]

        return uri_ref
