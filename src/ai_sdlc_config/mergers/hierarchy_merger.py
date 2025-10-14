"""
Core hierarchy merging logic inspired by C4H's deep_merge.

Key differences from C4H:
1. Works with HierarchyNode objects, not raw dicts
2. Preserves URI references instead of resolving them
3. Tracks merge provenance (which config each value came from)
4. Generic - no C4H-specific logic
"""
from typing import List, Dict, Any, Optional
from enum import Enum
import copy

from ..models.hierarchy_node import HierarchyNode, URIReference, NodeValue


class MergeStrategy(Enum):
    """
    Strategy for merging conflicting values.

    Inspired by C4H's merge rules but extended for URI handling.
    """
    OVERRIDE = "override"  # Later value completely replaces earlier (C4H default)
    PRESERVE = "preserve"  # Earlier value wins (opposite of OVERRIDE)
    URI_PRIORITY = "uri_priority"  # URI references take priority over direct values
    DEEP_MERGE = "deep_merge"  # Recursively merge nested structures


class HierarchyMerger:
    """
    Merges multiple HierarchyNode trees with priority-based overrides.

    Inspired by C4H's deep_merge() but designed for HierarchyNode structures.

    Key principles:
    1. Later hierarchies override earlier ones (configurable)
    2. URI references are preserved, not resolved during merge
    3. Nested structures are merged recursively
    4. Merge provenance is tracked
    """

    def __init__(self, strategy: MergeStrategy = MergeStrategy.OVERRIDE):
        self.strategy = strategy

    def merge(self, hierarchies: List[HierarchyNode]) -> HierarchyNode:
        """
        Merge multiple hierarchies into a single definitive hierarchy.

        Similar to C4H's approach in service.py:317-319 where multiple
        configs are merged sequentially with each one overriding the previous.

        Args:
            hierarchies: List of HierarchyNode roots, ordered by priority
                        (first = lowest priority, last = highest priority)

        Returns:
            Merged HierarchyNode tree

        Example:
            base = load_hierarchy("base.yml")
            prod = load_hierarchy("prod.yml")
            runtime = load_hierarchy("runtime.yml")

            # prod overrides base, runtime overrides both
            merged = merger.merge([base, prod, runtime])
        """
        if not hierarchies:
            raise ValueError("Cannot merge empty list of hierarchies")

        if len(hierarchies) == 1:
            return copy.deepcopy(hierarchies[0])

        # Start with first hierarchy as base
        result = copy.deepcopy(hierarchies[0])
        result.priority = 0
        result.source = f"merged_from_{len(hierarchies)}_sources"

        # Merge each subsequent hierarchy into result
        for i, hierarchy in enumerate(hierarchies[1:], start=1):
            result = self._merge_two_nodes(
                base=result,
                override=hierarchy,
                priority=i
            )

        return result

    def _merge_two_nodes(
        self,
        base: HierarchyNode,
        override: HierarchyNode,
        priority: int
    ) -> HierarchyNode:
        """
        Merge two HierarchyNode trees.

        Inspired by C4H's deep_merge() at config.py:304-378.

        Args:
            base: Base node (lower priority)
            override: Override node (higher priority)
            priority: Priority level for tracking

        Returns:
            Merged node
        """
        # Deep copy base to avoid mutation
        result = copy.deepcopy(base)
        result.priority = max(result.priority, priority)

        # If override is a leaf node with value, it wins (by default strategy)
        if override.is_leaf() and override.value is not None:
            if self.strategy == MergeStrategy.OVERRIDE:
                result.value = copy.deepcopy(override.value)
                result.source = override.source
                result.priority = priority
                result.children = {}  # Replace any children
            elif self.strategy == MergeStrategy.URI_PRIORITY:
                # If override has URI, it wins; if base has URI and override doesn't, base wins
                if isinstance(override.value, URIReference):
                    result.value = copy.deepcopy(override.value)
                    result.source = override.source
                    result.priority = priority
                    result.children = {}
                elif not isinstance(result.value, URIReference):
                    # Neither has URI, use normal override
                    result.value = copy.deepcopy(override.value)
                    result.source = override.source
                    result.priority = priority
                    result.children = {}
                # Else: base has URI, override doesn't -> keep base

        # If override is a container, merge children recursively
        if override.is_container():
            # First, ensure result is also a container
            if result.is_leaf():
                # Override transforms leaf to container - depends on strategy
                if self.strategy == MergeStrategy.OVERRIDE:
                    result.value = None
                    result.children = {}

            # Merge each child from override
            for key, override_child in override.children.items():
                if key in result.children:
                    # Child exists in both - merge recursively
                    result.children[key] = self._merge_two_nodes(
                        base=result.children[key],
                        override=override_child,
                        priority=priority
                    )
                else:
                    # Child only in override - add it
                    result.children[key] = copy.deepcopy(override_child)
                    result.children[key].priority = priority

        return result

    def merge_with_overrides(
        self,
        base: HierarchyNode,
        overrides: Dict[str, Any]
    ) -> HierarchyNode:
        """
        Merge a base hierarchy with specific path overrides.

        Useful for runtime configuration where you want to override
        specific paths without loading a full hierarchy.

        Args:
            base: Base hierarchy
            overrides: Dict of path -> value overrides
                      e.g., {"system.agents.discovery.model": "claude-3-5-sonnet"}

        Returns:
            Merged hierarchy with overrides applied

        Example:
            config = load_hierarchy("base.yml")
            overrides = {
                "llm.agents.discovery.model": "claude-3-7-sonnet",
                "llm.providers.anthropic.api_key": URIReference("env://ANTHROPIC_API_KEY")
            }
            merged = merger.merge_with_overrides(config, overrides)
        """
        result = copy.deepcopy(base)

        for path, value in overrides.items():
            self._set_value_at_path(result, path, value)

        return result

    def _set_value_at_path(
        self,
        root: HierarchyNode,
        path: str,
        value: NodeValue
    ) -> None:
        """
        Set value at specific path in hierarchy, creating nodes as needed.

        Args:
            root: Root node
            path: Dot-delimited path
            value: Value to set
        """
        parts = path.split('.')
        current = root

        # Navigate to parent of target node, creating as needed
        for part in parts[:-1]:
            if part not in current.children:
                new_path = f"{current.path}.{part}" if current.path else part
                current.children[part] = HierarchyNode(
                    path=new_path,
                    source="runtime_override"
                )
            current = current.children[part]

        # Set value on final node
        final_key = parts[-1]
        if final_key not in current.children:
            new_path = f"{current.path}.{final_key}" if current.path else final_key
            current.children[final_key] = HierarchyNode(
                path=new_path,
                source="runtime_override"
            )

        target = current.children[final_key]
        target.value = value
        target.children = {}  # Clear any children when setting value


class MergeReport:
    """
    Report of merge operation showing what was merged and from where.

    Useful for debugging and auditing configuration.
    """

    def __init__(self):
        self.merged_paths: List[str] = []
        self.conflicts: List[Dict[str, Any]] = []
        self.uri_references: List[Dict[str, Any]] = []

    def add_merge(self, path: str, base_source: str, override_source: str):
        """Record a merge operation"""
        self.merged_paths.append(path)
        self.conflicts.append({
            "path": path,
            "base_source": base_source,
            "override_source": override_source,
            "resolution": "override_wins"
        })

    def add_uri_reference(self, path: str, uri: str, source: str):
        """Record a URI reference"""
        self.uri_references.append({
            "path": path,
            "uri": uri,
            "source": source
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary"""
        return {
            "total_merges": len(self.merged_paths),
            "conflicts": self.conflicts,
            "uri_references": self.uri_references
        }
