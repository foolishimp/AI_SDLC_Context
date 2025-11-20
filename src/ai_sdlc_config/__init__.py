"""
ai_sdlc_method - Generic URI-based dot hierarchy configuration merging system

This library provides a flexible way to manage configuration using:
1. Dot hierarchy paths (e.g., "system.agents.discovery")
2. URI references to external content
3. Priority-based merging of multiple config sources

Inspired by the C4H configuration system but designed to be generic
and work with any content type at any URI.
"""
from .models import HierarchyNode, URIReference, NodeValue
from .loaders import YAMLLoader, URIResolver
from .mergers import HierarchyMerger, MergeStrategy
from .core import ConfigManager

__version__ = "0.1.0"

__all__ = [
    "HierarchyNode",
    "URIReference",
    "NodeValue",
    "YAMLLoader",
    "URIResolver",
    "HierarchyMerger",
    "MergeStrategy",
    "ConfigManager",
]
