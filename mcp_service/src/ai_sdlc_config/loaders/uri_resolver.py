"""
URI resolution - fetch content from various URI schemes.

This is the key component that enables content to live anywhere:
- Local files
- Remote HTTP/HTTPS resources
- Inline data URIs
- Cross-references to other hierarchy nodes
"""
from typing import Optional, Dict, Any, Callable
from pathlib import Path
from urllib.parse import urlparse
import urllib.request

from ..models.hierarchy_node import URIReference, URIScheme, HierarchyNode


class URIResolver:
    """
    Resolves URIs to content.

    Supports:
    - file:// - Local file system
    - http(s):// - Web resources
    - data: - Inline data URIs
    - ref: - References to other nodes in hierarchy

    Extensible: Can register custom schemes
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize resolver.

        Args:
            base_path: Base path for resolving relative file URIs
        """
        self.base_path = base_path or Path.cwd()
        self.cache: Dict[str, str] = {}  # URI -> content cache
        self.custom_resolvers: Dict[str, Callable] = {}

    def resolve(self, uri_ref: URIReference, hierarchy: Optional[HierarchyNode] = None) -> str:
        """
        Resolve URI reference to content.

        Args:
            uri_ref: URIReference to resolve
            hierarchy: Optional hierarchy for resolving ref: URIs

        Returns:
            Content as string

        Raises:
            ValueError: If scheme is unsupported
            FileNotFoundError: If file:// URI not found
            urllib.error.URLError: If http(s):// fetch fails
        """
        # Check cache first
        if uri_ref.uri in self.cache:
            return self.cache[uri_ref.uri]

        # Route to appropriate resolver
        if uri_ref.scheme == URIScheme.FILE:
            content = self._resolve_file(uri_ref)
        elif uri_ref.scheme in (URIScheme.HTTP, URIScheme.HTTPS):
            content = self._resolve_http(uri_ref)
        elif uri_ref.scheme == URIScheme.DATA:
            content = self._resolve_data(uri_ref)
        elif uri_ref.scheme == URIScheme.REF:
            if hierarchy is None:
                raise ValueError("Cannot resolve ref: URI without hierarchy context")
            content = self._resolve_ref(uri_ref, hierarchy)
        else:
            # Try custom resolver
            if uri_ref.scheme.value in self.custom_resolvers:
                content = self.custom_resolvers[uri_ref.scheme.value](uri_ref)
            else:
                raise ValueError(f"Unsupported URI scheme: {uri_ref.scheme}")

        # Cache the result
        self.cache[uri_ref.uri] = content
        return content

    def _resolve_file(self, uri_ref: URIReference) -> str:
        """
        Resolve file:// URI.

        Examples:
            file:///absolute/path/to/file.md
            file://relative/path/to/file.md
        """
        # Remove file:// prefix
        file_path = uri_ref.uri.replace("file://", "")

        # Convert to Path
        path = Path(file_path)

        # If relative, resolve against base_path
        if not path.is_absolute():
            path = self.base_path / path

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Read content
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _resolve_http(self, uri_ref: URIReference) -> str:
        """
        Resolve http:// or https:// URI.

        Example:
            https://docs.example.com/prompts/discovery.md
        """
        with urllib.request.urlopen(uri_ref.uri) as response:
            content = response.read()
            # Decode assuming UTF-8 (could be smarter about encoding)
            return content.decode('utf-8')

    def _resolve_data(self, uri_ref: URIReference) -> str:
        """
        Resolve data: URI (inline content).

        Example:
            data:text/plain;base64,SGVsbG8gV29ybGQ=
            data:text/plain,Hello%20World
        """
        # Parse data URI
        # Format: data:[<mediatype>][;base64],<data>
        uri = uri_ref.uri
        if not uri.startswith("data:"):
            raise ValueError(f"Invalid data URI: {uri}")

        # Split into metadata and data
        parts = uri[5:].split(',', 1)  # Remove "data:" prefix
        if len(parts) != 2:
            raise ValueError(f"Invalid data URI format: {uri}")

        metadata, data = parts

        # Check if base64 encoded
        if ";base64" in metadata:
            import base64
            return base64.b64decode(data).decode('utf-8')
        else:
            # URL decode
            from urllib.parse import unquote
            return unquote(data)

    def _resolve_ref(self, uri_ref: URIReference, hierarchy: HierarchyNode) -> str:
        """
        Resolve ref: URI (reference to another node in hierarchy).

        Example:
            ref:system.base.prompts.default

        This allows sharing content across multiple config paths.
        """
        # Extract path from ref: URI
        ref_path = uri_ref.uri.replace("ref:", "")

        # Look up node in hierarchy
        target_node = hierarchy.get_node_by_path(ref_path)
        if target_node is None:
            raise ValueError(f"Reference not found: {ref_path}")

        # Get value from target node
        if isinstance(target_node.value, URIReference):
            # Recursively resolve if target is also a URI
            return self.resolve(target_node.value, hierarchy)
        elif isinstance(target_node.value, str):
            return target_node.value
        else:
            raise ValueError(f"Cannot resolve ref to non-string value at {ref_path}")

    def register_custom_resolver(
        self,
        scheme: str,
        resolver: Callable[[URIReference], str]
    ) -> None:
        """
        Register custom URI scheme resolver.

        Example:
            def resolve_s3(uri_ref):
                # Fetch from S3
                return boto3.client('s3').get_object(...)['Body'].read()

            resolver.register_custom_resolver("s3", resolve_s3)

        Args:
            scheme: URI scheme (e.g., "s3", "git", "env")
            resolver: Function that takes URIReference and returns content string
        """
        self.custom_resolvers[scheme] = resolver

    def clear_cache(self) -> None:
        """Clear the content cache"""
        self.cache.clear()
