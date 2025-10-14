"""
Core data models for representing hierarchical configuration with URI references.

This module defines the fundamental building blocks:
- HierarchyNode: Represents a node in the dot hierarchy
- URIReference: Represents a reference to external content
- NodeValue: Union type for values that can be stored in nodes
"""
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from enum import Enum


class URIScheme(Enum):
    """Supported URI schemes"""
    FILE = "file"
    HTTP = "http"
    HTTPS = "https"
    DATA = "data"  # data: inline content
    REF = "ref"    # ref: reference to another node in hierarchy


@dataclass
class URIReference:
    """
    Represents a reference to content at a URI.

    This is the key abstraction that separates structure from content.
    Instead of embedding large text blocks, we reference where to find them.

    Examples:
        file:///prompts/discovery.md
        https://docs.example.com/api/v1/prompts/coder
        data:text/plain;base64,SGVsbG8gV29ybGQ=
        ref:system.base.prompts.default
    """
    uri: str
    scheme: URIScheme
    content_type: Optional[str] = None  # e.g., "text/markdown", "application/json"
    metadata: Dict[str, Any] = field(default_factory=dict)  # version, checksum, etc.

    @staticmethod
    def from_string(uri: str) -> 'URIReference':
        """Create URIReference from URI string"""
        if "://" not in uri:
            # Assume file path
            uri = f"file://{uri}"

        scheme_str = uri.split("://")[0].lower()
        try:
            scheme = URIScheme(scheme_str)
        except ValueError:
            raise ValueError(f"Unsupported URI scheme: {scheme_str}")

        return URIReference(uri=uri, scheme=scheme)

    def __repr__(self) -> str:
        return f"URIReference(uri='{self.uri}')"


# NodeValue can be:
# - A primitive (str, int, bool, etc.)
# - A URIReference (pointer to external content)
# - A dict (nested structure)
# - A list (array of values)
NodeValue = Union[str, int, float, bool, None, URIReference, Dict[str, Any], List[Any]]


@dataclass
class HierarchyNode:
    """
    Represents a node in the dot hierarchy.

    Key design principles:
    1. Each node has a path (e.g., "system.agents.discovery")
    2. Nodes can contain direct values OR URI references
    3. Nodes can have children (nested structure)
    4. Nodes track their source (which config file they came from)

    Inspired by C4H's ConfigNode but designed for URI-based content.
    """
    path: str  # Dot-delimited path (e.g., "system.agents.discovery")
    value: Optional[NodeValue] = None  # Direct value if not a container
    children: Dict[str, 'HierarchyNode'] = field(default_factory=dict)
    source: Optional[str] = None  # Which config file this came from
    priority: int = 0  # Merge priority (higher wins)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_uri_reference(self) -> bool:
        """Check if this node contains a URI reference"""
        return isinstance(self.value, URIReference)

    def is_container(self) -> bool:
        """Check if this node is a container (has children)"""
        return len(self.children) > 0

    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has value, no children)"""
        return self.value is not None and not self.is_container()

    def get_child(self, key: str) -> Optional['HierarchyNode']:
        """Get immediate child by key"""
        return self.children.get(key)

    def add_child(self, key: str, node: 'HierarchyNode') -> None:
        """Add child node"""
        self.children[key] = node

    def get_value_by_path(self, path: str) -> Optional[NodeValue]:
        """
        Get value at dot-delimited path relative to this node.

        Similar to C4H's ConfigNode.get_value()

        Args:
            path: Dot-delimited path (e.g., "agents.discovery.model")

        Returns:
            Value at path or None if not found
        """
        if not path:
            return self.value

        parts = path.split('.')
        current = self

        for part in parts:
            if part not in current.children:
                return None
            current = current.children[part]

        return current.value

    def get_node_by_path(self, path: str) -> Optional['HierarchyNode']:
        """
        Get node at dot-delimited path relative to this node.

        Similar to C4H's ConfigNode.get_node()
        """
        if not path:
            return self

        parts = path.split('.')
        current = self

        for part in parts:
            if part not in current.children:
                return None
            current = current.children[part]

        return current

    def find_all_by_pattern(self, pattern: str) -> List[tuple[str, 'HierarchyNode']]:
        """
        Find all nodes matching a wildcard pattern.

        Similar to C4H's ConfigNode.find_all()

        Args:
            pattern: Dot-delimited pattern with wildcards (e.g., "agents.*.model")

        Returns:
            List of (path, node) tuples
        """
        results = []
        self._find_recursive(pattern.split('.'), [], results)
        return results

    def _find_recursive(
        self,
        pattern_parts: List[str],
        current_path: List[str],
        results: List[tuple[str, 'HierarchyNode']]
    ) -> None:
        """Recursive helper for pattern matching"""
        if not pattern_parts:
            # Matched entire pattern
            results.append(('.'.join(current_path), self))
            return

        current_pattern = pattern_parts[0]
        remaining_pattern = pattern_parts[1:]

        if current_pattern == '*':
            # Wildcard matches any key
            for key, child in self.children.items():
                child._find_recursive(
                    remaining_pattern,
                    current_path + [key],
                    results
                )
        else:
            # Exact match
            if current_pattern in self.children:
                self.children[current_pattern]._find_recursive(
                    remaining_pattern,
                    current_path + [current_pattern],
                    results
                )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert node tree to dictionary representation.
        Useful for serialization and debugging.
        """
        if self.is_leaf():
            if isinstance(self.value, URIReference):
                return {
                    "_uri": self.value.uri,
                    "_type": "uri_reference"
                }
            return self.value

        result = {}
        for key, child in self.children.items():
            result[key] = child.to_dict()

        return result

    def __repr__(self) -> str:
        value_repr = f"value={self.value}" if not self.is_container() else f"children={len(self.children)}"
        return f"HierarchyNode(path='{self.path}', {value_repr})"
