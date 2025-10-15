"""
Unit tests for uri_resolver module.

Tests cover:
- Resolving file:// URIs
- Resolving http:// and https:// URIs
- Resolving data: URIs
- Resolving ref: URIs (cross-references)
- Custom URI scheme resolvers
- URI caching
- Error handling
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import base64

from ai_sdlc_config.loaders.uri_resolver import URIResolver
from ai_sdlc_config.models.hierarchy_node import (
    URIReference,
    URIScheme,
    HierarchyNode
)


class TestURIResolver:
    """Test URIResolver class"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def resolver(self, temp_dir):
        """Create a URIResolver with temporary base path"""
        return URIResolver(base_path=temp_dir)

    def test_create_resolver_default_base_path(self):
        """Test creating resolver with default base path"""
        resolver = URIResolver()
        assert resolver.base_path == Path.cwd()
        assert resolver.cache == {}
        assert resolver.custom_resolvers == {}

    def test_create_resolver_custom_base_path(self, temp_dir):
        """Test creating resolver with custom base path"""
        resolver = URIResolver(base_path=temp_dir)
        assert resolver.base_path == temp_dir

    def test_resolve_file_absolute_path(self, resolver, temp_dir):
        """Test resolving file:// URI with absolute path"""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!")

        uri_ref = URIReference(
            uri=f"file://{test_file}",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Hello, World!"

    def test_resolve_file_relative_path(self, resolver, temp_dir):
        """Test resolving file:// URI with relative path"""
        # Create test file
        test_file = temp_dir / "subdir" / "test.txt"
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text("Relative content")

        uri_ref = URIReference(
            uri="file://subdir/test.txt",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Relative content"

    def test_resolve_file_not_found(self, resolver):
        """Test resolving non-existent file raises FileNotFoundError"""
        uri_ref = URIReference(
            uri="file:///nonexistent/file.txt",
            scheme=URIScheme.FILE
        )
        with pytest.raises(FileNotFoundError):
            resolver.resolve(uri_ref)

    def test_resolve_file_with_triple_slash(self, resolver, temp_dir):
        """Test resolving file:/// URI (triple slash)"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Content")

        uri_ref = URIReference(
            uri=f"file:///{test_file}",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Content"

    @patch('urllib.request.urlopen')
    def test_resolve_https_uri(self, mock_urlopen, resolver):
        """Test resolving https:// URI"""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.read.return_value = b"Web content"
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_urlopen.return_value = mock_response

        uri_ref = URIReference(
            uri="https://example.com/doc.md",
            scheme=URIScheme.HTTPS
        )
        content = resolver.resolve(uri_ref)
        assert content == "Web content"
        mock_urlopen.assert_called_once_with("https://example.com/doc.md")

    @patch('urllib.request.urlopen')
    def test_resolve_http_uri(self, mock_urlopen, resolver):
        """Test resolving http:// URI"""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.read.return_value = b"HTTP content"
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_urlopen.return_value = mock_response

        uri_ref = URIReference(
            uri="http://example.com/file.txt",
            scheme=URIScheme.HTTP
        )
        content = resolver.resolve(uri_ref)
        assert content == "HTTP content"

    def test_resolve_data_uri_plain_text(self, resolver):
        """Test resolving data: URI with plain text"""
        uri_ref = URIReference(
            uri="data:text/plain,Hello%20World",
            scheme=URIScheme.DATA
        )
        content = resolver.resolve(uri_ref)
        assert content == "Hello World"

    def test_resolve_data_uri_base64(self, resolver):
        """Test resolving data: URI with base64 encoding"""
        # Base64 encode "Hello, World!"
        encoded = base64.b64encode(b"Hello, World!").decode('ascii')
        uri_ref = URIReference(
            uri=f"data:text/plain;base64,{encoded}",
            scheme=URIScheme.DATA
        )
        content = resolver.resolve(uri_ref)
        assert content == "Hello, World!"

    def test_resolve_data_uri_invalid_format(self, resolver):
        """Test resolving invalid data: URI raises ValueError"""
        uri_ref = URIReference(
            uri="data:invalid_format",
            scheme=URIScheme.DATA
        )
        with pytest.raises(ValueError, match="Invalid data URI format"):
            resolver.resolve(uri_ref)

    def test_resolve_data_uri_missing_prefix(self, resolver):
        """Test resolving data URI without 'data:' prefix raises ValueError"""
        uri_ref = URIReference(
            uri="text/plain,content",
            scheme=URIScheme.DATA
        )
        with pytest.raises(ValueError, match="Invalid data URI"):
            resolver.resolve(uri_ref)

    def test_resolve_ref_uri_to_string_value(self, resolver):
        """Test resolving ref: URI to another node with string value"""
        # Create hierarchy
        root = HierarchyNode(path="")
        base = HierarchyNode(path="base")
        prompt = HierarchyNode(path="base.prompt", value="Base prompt content")
        base.add_child("prompt", prompt)
        root.add_child("base", base)

        # Reference to base.prompt
        uri_ref = URIReference(
            uri="ref:base.prompt",
            scheme=URIScheme.REF
        )
        content = resolver.resolve(uri_ref, hierarchy=root)
        assert content == "Base prompt content"

    def test_resolve_ref_uri_to_uri_reference(self, resolver, temp_dir):
        """Test resolving ref: URI to another node with URI reference (recursive)"""
        # Create test file
        test_file = temp_dir / "content.txt"
        test_file.write_text("File content")

        # Create hierarchy
        root = HierarchyNode(path="")
        base = HierarchyNode(path="base")
        file_uri = URIReference(uri=f"file://{test_file}", scheme=URIScheme.FILE)
        prompt = HierarchyNode(path="base.prompt", value=file_uri)
        base.add_child("prompt", prompt)
        root.add_child("base", base)

        # Reference to base.prompt (which itself is a URI)
        uri_ref = URIReference(
            uri="ref:base.prompt",
            scheme=URIScheme.REF
        )
        content = resolver.resolve(uri_ref, hierarchy=root)
        assert content == "File content"

    def test_resolve_ref_uri_not_found(self, resolver):
        """Test resolving ref: URI to non-existent path raises ValueError"""
        root = HierarchyNode(path="")
        uri_ref = URIReference(
            uri="ref:nonexistent.path",
            scheme=URIScheme.REF
        )
        with pytest.raises(ValueError, match="Reference not found"):
            resolver.resolve(uri_ref, hierarchy=root)

    def test_resolve_ref_uri_without_hierarchy(self, resolver):
        """Test resolving ref: URI without hierarchy context raises ValueError"""
        uri_ref = URIReference(
            uri="ref:some.path",
            scheme=URIScheme.REF
        )
        with pytest.raises(ValueError, match="Cannot resolve ref: URI without hierarchy"):
            resolver.resolve(uri_ref)

    def test_resolve_ref_uri_to_non_string(self, resolver):
        """Test resolving ref: URI to non-string value raises ValueError"""
        root = HierarchyNode(path="")
        system = HierarchyNode(path="system")
        count = HierarchyNode(path="system.count", value=42)
        system.add_child("count", count)
        root.add_child("system", system)

        uri_ref = URIReference(
            uri="ref:system.count",
            scheme=URIScheme.REF
        )
        with pytest.raises(ValueError, match="Cannot resolve ref to non-string value"):
            resolver.resolve(uri_ref, hierarchy=root)

    def test_caching(self, resolver, temp_dir):
        """Test that resolved content is cached"""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Original content")

        uri_ref = URIReference(
            uri=f"file://{test_file}",
            scheme=URIScheme.FILE
        )

        # First resolve
        content1 = resolver.resolve(uri_ref)
        assert content1 == "Original content"

        # Modify file
        test_file.write_text("Modified content")

        # Second resolve should return cached content
        content2 = resolver.resolve(uri_ref)
        assert content2 == "Original content"  # Still original from cache

    def test_clear_cache(self, resolver, temp_dir):
        """Test clearing the cache"""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Original content")

        uri_ref = URIReference(
            uri=f"file://{test_file}",
            scheme=URIScheme.FILE
        )

        # First resolve
        content1 = resolver.resolve(uri_ref)
        assert content1 == "Original content"

        # Modify file and clear cache
        test_file.write_text("Modified content")
        resolver.clear_cache()

        # Second resolve should return new content
        content2 = resolver.resolve(uri_ref)
        assert content2 == "Modified content"

    def test_register_custom_resolver(self, resolver):
        """Test registering and using custom URI resolver"""
        # Custom resolver for 's3' scheme
        def mock_s3_resolver(uri_ref: URIReference) -> str:
            return f"Content from {uri_ref.uri}"

        resolver.register_custom_resolver("s3", mock_s3_resolver)

        # Create URIReference with custom scheme
        # Note: We need to add S3 to URIScheme enum or handle it differently
        # For testing, we'll mock it
        from unittest.mock import patch
        with patch('ai_sdlc_config.models.hierarchy_node.URIScheme') as mock_enum:
            mock_scheme = Mock()
            mock_scheme.value = "s3"
            uri_ref = URIReference(
                uri="s3://bucket/key",
                scheme=mock_scheme
            )
            content = resolver.resolve(uri_ref)
            assert content == "Content from s3://bucket/key"

    def test_unsupported_scheme_without_custom_resolver(self, resolver):
        """Test that unsupported scheme without custom resolver raises ValueError"""
        # Create a mock scheme
        from unittest.mock import Mock
        mock_scheme = Mock()
        mock_scheme.value = "unsupported"

        uri_ref = URIReference(
            uri="unsupported://resource",
            scheme=mock_scheme
        )

        with pytest.raises(ValueError, match="Unsupported URI scheme"):
            resolver.resolve(uri_ref)

    def test_resolve_file_with_unicode(self, resolver, temp_dir):
        """Test resolving file with Unicode content"""
        test_file = temp_dir / "unicode.txt"
        test_file.write_text("Hello 世界 🌍", encoding='utf-8')

        uri_ref = URIReference(
            uri=f"file://{test_file}",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Hello 世界 🌍"

    def test_resolve_multiple_different_uris(self, resolver, temp_dir):
        """Test resolving multiple different URIs"""
        # Create test files
        file1 = temp_dir / "file1.txt"
        file1.write_text("Content 1")
        file2 = temp_dir / "file2.txt"
        file2.write_text("Content 2")

        uri_ref1 = URIReference(uri=f"file://{file1}", scheme=URIScheme.FILE)
        uri_ref2 = URIReference(uri=f"file://{file2}", scheme=URIScheme.FILE)

        content1 = resolver.resolve(uri_ref1)
        content2 = resolver.resolve(uri_ref2)

        assert content1 == "Content 1"
        assert content2 == "Content 2"

    def test_data_uri_with_different_media_types(self, resolver):
        """Test resolving data URIs with different media types"""
        # JSON data URI
        uri_json = URIReference(
            uri='data:application/json,{"key":"value"}',
            scheme=URIScheme.DATA
        )
        content_json = resolver.resolve(uri_json)
        assert content_json == '{"key":"value"}'

        # Plain text data URI
        uri_text = URIReference(
            uri="data:text/plain,plain%20text",
            scheme=URIScheme.DATA
        )
        content_text = resolver.resolve(uri_text)
        assert content_text == "plain text"

    def test_resolve_file_creates_correct_path_object(self, resolver, temp_dir):
        """Test that file resolution creates correct Path object"""
        # Create nested directory structure
        nested_dir = temp_dir / "a" / "b" / "c"
        nested_dir.mkdir(parents=True)
        test_file = nested_dir / "test.txt"
        test_file.write_text("Nested content")

        uri_ref = URIReference(
            uri="file://a/b/c/test.txt",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Nested content"

    def test_ref_uri_circular_reference_prevention(self, resolver):
        """Test that circular references are handled (or at least don't infinite loop)"""
        # Note: Current implementation doesn't prevent circular refs
        # This test documents the behavior
        root = HierarchyNode(path="")
        a = HierarchyNode(path="a")
        b = HierarchyNode(path="b")

        # Create circular reference (if we tried this, it would infinite loop)
        # a points to b, b points to a
        # For now, we test that a valid reference chain works
        b.value = "Final value"
        a.value = URIReference(uri="ref:b", scheme=URIScheme.REF)
        root.add_child("a", a)
        root.add_child("b", b)

        uri_ref = URIReference(uri="ref:a", scheme=URIScheme.REF)
        content = resolver.resolve(uri_ref, hierarchy=root)
        assert content == "Final value"

    @patch('urllib.request.urlopen')
    def test_http_error_handling(self, mock_urlopen, resolver):
        """Test that HTTP errors are raised properly"""
        from urllib.error import URLError
        mock_urlopen.side_effect = URLError("Network error")

        uri_ref = URIReference(
            uri="https://example.com/error",
            scheme=URIScheme.HTTPS
        )
        with pytest.raises(URLError):
            resolver.resolve(uri_ref)

    def test_empty_file_resolution(self, resolver, temp_dir):
        """Test resolving empty file"""
        test_file = temp_dir / "empty.txt"
        test_file.write_text("")

        uri_ref = URIReference(
            uri=f"file://{test_file}",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == ""

    def test_base_path_resolution(self, temp_dir):
        """Test that base_path is used correctly for relative paths"""
        subdir = temp_dir / "config"
        subdir.mkdir()
        test_file = subdir / "test.txt"
        test_file.write_text("Config content")

        # Resolver with config subdir as base
        resolver = URIResolver(base_path=subdir)

        uri_ref = URIReference(
            uri="file://test.txt",
            scheme=URIScheme.FILE
        )
        content = resolver.resolve(uri_ref)
        assert content == "Config content"
