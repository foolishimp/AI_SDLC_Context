"""
High-level API for working with hierarchical configuration.

# Implements: REQ-NFR-FEDERATE-001 (Hierarchical configuration composition)

This provides a simple interface that combines loading, merging, and resolving.
Similar to how C4H uses configurations, but generic and URI-based.
"""
from typing import List, Optional, Any, Dict
from pathlib import Path

from ..models import HierarchyNode, URIReference, NodeValue
from ..loaders import YAMLLoader, URIResolver
from ..mergers import HierarchyMerger, MergeStrategy


class ConfigManager:
    """
    High-level configuration manager.

    Provides a simple API for:
    1. Loading configurations from YAML files
    2. Merging multiple configurations with priority
    3. Accessing values using dot notation
    4. Resolving URI references to content

    Example:
        # Create manager
        manager = ConfigManager()

        # Load configurations (priority order: base < prod < runtime)
        manager.load_hierarchy("config/base.yml")
        manager.load_hierarchy("config/production.yml")
        manager.add_runtime_overrides({
            "system.agents.discovery.model": "claude-3-7-sonnet"
        })

        # Merge all configurations
        manager.merge()

        # Access values
        model = manager.get_value("system.agents.discovery.model")
        prompt_uri = manager.get_uri("system.agents.discovery.prompt")
        prompt_content = manager.get_content("system.agents.discovery.prompt")
    """

    def __init__(
        self,
        base_path: Optional[Path] = None,
        merge_strategy: MergeStrategy = MergeStrategy.OVERRIDE
    ):
        """
        Initialize configuration manager.

        Args:
            base_path: Base path for resolving relative file URIs and config files
            merge_strategy: Strategy for merging conflicts
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.loader = YAMLLoader()
        self.resolver = URIResolver(self.base_path)
        self.merger = HierarchyMerger(merge_strategy)

        self.hierarchies: List[HierarchyNode] = []
        self.merged_hierarchy: Optional[HierarchyNode] = None

    def load_hierarchy(self, file_path: str, source_name: Optional[str] = None) -> None:
        """
        Load a configuration hierarchy from YAML file.

        Args:
            file_path: Path to YAML configuration file (absolute or relative to base_path)
            source_name: Optional name for tracking (defaults to file_path)
        """
        # Resolve path relative to base_path if not absolute
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path

        hierarchy = self.loader.load(str(path), source_name)
        self.hierarchies.append(hierarchy)
        # Clear merged hierarchy - needs re-merge
        self.merged_hierarchy = None

    def load_hierarchy_from_string(self, yaml_string: str, source_name: str) -> None:
        """
        Load a configuration hierarchy from YAML string.

        Args:
            yaml_string: YAML content as string
            source_name: Name for tracking source
        """
        hierarchy = self.loader.load_from_string(yaml_string, source_name)
        self.hierarchies.append(hierarchy)
        self.merged_hierarchy = None

    def add_runtime_overrides(self, overrides: Dict[str, Any]) -> None:
        """
        Add runtime overrides as highest priority configuration.

        Similar to C4H's runtime config merging in service.py

        Args:
            overrides: Dict of path -> value overrides
        """
        # Create a hierarchy from overrides
        runtime_hierarchy = HierarchyNode(path="", source="runtime_overrides")

        # Build hierarchy from flat dict
        for path, value in overrides.items():
            self._add_path_to_hierarchy(runtime_hierarchy, path, value)

        self.hierarchies.append(runtime_hierarchy)
        self.merged_hierarchy = None

    def _add_path_to_hierarchy(
        self,
        root: HierarchyNode,
        path: str,
        value: Any
    ) -> None:
        """Helper to add a path to hierarchy"""
        parts = path.split('.')
        current = root

        for i, part in enumerate(parts[:-1]):
            if part not in current.children:
                node_path = '.'.join(parts[:i+1])
                current.children[part] = HierarchyNode(
                    path=node_path,
                    source="runtime_overrides"
                )
            current = current.children[part]

        # Add final node with value
        final_key = parts[-1]
        final_path = '.'.join(parts)
        current.children[final_key] = HierarchyNode(
            path=final_path,
            value=value,
            source="runtime_overrides"
        )

    def merge(self) -> None:
        """
        Merge all loaded hierarchies into a single definitive hierarchy.

        Hierarchies are merged in the order they were loaded, with later
        hierarchies having higher priority (overriding earlier ones).

        Similar to C4H's sequential merging in service.py:317-319
        """
        if not self.hierarchies:
            raise ValueError("No hierarchies loaded to merge")

        self.merged_hierarchy = self.merger.merge(self.hierarchies)

    def get_value(self, path: str) -> Optional[NodeValue]:
        """
        Get value at path in merged hierarchy.

        If value is a URIReference, returns the URIReference object.
        Use get_content() to resolve URI to content.

        Args:
            path: Dot-delimited path

        Returns:
            Value at path or None if not found

        Raises:
            ValueError: If hierarchy not yet merged
        """
        if self.merged_hierarchy is None:
            raise ValueError("Hierarchy not merged. Call merge() first.")

        return self.merged_hierarchy.get_value_by_path(path)

    def get_uri(self, path: str) -> Optional[str]:
        """
        Get URI string at path if value is a URI reference.

        Args:
            path: Dot-delimited path

        Returns:
            URI string or None if not a URI reference
        """
        value = self.get_value(path)
        if isinstance(value, URIReference):
            return value.uri
        return None

    def get_content(self, path: str) -> Optional[str]:
        """
        Get content at path, resolving URI if necessary.

        If value is a URIReference, resolves it to content.
        If value is a string, returns it directly.

        Args:
            path: Dot-delimited path

        Returns:
            Content as string or None if not found

        Raises:
            ValueError: If hierarchy not yet merged
        """
        value = self.get_value(path)

        if value is None:
            return None
        elif isinstance(value, URIReference):
            return self.resolver.resolve(value, self.merged_hierarchy)
        elif isinstance(value, str):
            return value
        else:
            # Convert other types to string
            return str(value)

    def get_node(self, path: str) -> Optional[HierarchyNode]:
        """
        Get node at path in merged hierarchy.

        Useful for exploring structure or working with sub-trees.

        Args:
            path: Dot-delimited path

        Returns:
            HierarchyNode or None if not found
        """
        if self.merged_hierarchy is None:
            raise ValueError("Hierarchy not merged. Call merge() first.")

        return self.merged_hierarchy.get_node_by_path(path)

    def find_all(self, pattern: str) -> List[tuple[str, HierarchyNode]]:
        """
        Find all nodes matching wildcard pattern.

        Args:
            pattern: Dot-delimited pattern with wildcards (e.g., "system.agents.*")

        Returns:
            List of (path, node) tuples
        """
        if self.merged_hierarchy is None:
            raise ValueError("Hierarchy not merged. Call merge() first.")

        return self.merged_hierarchy.find_all_by_pattern(pattern)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert merged hierarchy to dictionary representation.

        Useful for debugging and serialization.

        Returns:
            Dictionary representation of hierarchy
        """
        if self.merged_hierarchy is None:
            raise ValueError("Hierarchy not merged. Call merge() first.")

        return self.merged_hierarchy.to_dict()

    def register_uri_resolver(
        self,
        scheme: str,
        resolver_func: callable
    ) -> None:
        """
        Register custom URI scheme resolver.

        Args:
            scheme: URI scheme (e.g., "s3", "vault")
            resolver_func: Function that takes URIReference and returns content
        """
        self.resolver.register_custom_resolver(scheme, resolver_func)
