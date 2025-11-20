#!/usr/bin/env python3
"""Setup script for MCP service."""
from setuptools import setup, find_packages

setup(
    name="ai-sdlc-config-mcp",
    version="0.1.0",
    description="MCP service for ai_sdlc_method project management",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "mcp>=0.9.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ai-sdlc-mcp=server.main:main",
        ],
    },
)
