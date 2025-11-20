# Installers Directory

Python-based installers and setup scripts for the AI SDLC Method.

## Purpose

This directory contains installation scripts for setting up the AI SDLC methodology using Python scripts instead of Claude Code's native plugin system.

## Available Installers

### Coming Soon

This directory is reserved for future Python-based installation tools:

- **setup_plugins.py** - Install plugins programmatically
- **setup_mcp.py** - Configure MCP service
- **install_all.py** - Complete AI SDLC setup wizard

## Current Installation Methods

For now, use the standard installation methods:

### Method 1: Claude Code Plugins (Recommended)
```bash
/plugin marketplace add foolishimp/ai_sdlc_method
/plugin install @aisdlc/aisdlc-methodology
```

### Method 2: MCP Service
```bash
cd mcp_service
pip install -e .
python -m server.main --stdio
```

See [../README.md](../README.md) for complete installation instructions.
