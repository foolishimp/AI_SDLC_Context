#!/usr/bin/env python3
"""
Advanced usage example for AI_SDLC_Context

This demonstrates:
1. Merging base + environment + user configs (3 layers)
2. Using ref: URIs to share content
3. Custom URI resolver
4. Comparing different merge strategies
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_sdlc_config import ConfigManager, MergeStrategy, URIReference


def demo_three_layer_merge():
    """
    Demonstrate merging 3 config layers:
    base.yml < production.yml < runtime overrides
    """
    print("=== Three-Layer Merge Demo ===\n")

    examples_dir = Path(__file__).parent
    manager = ConfigManager(base_path=examples_dir)

    # Layer 1: Base defaults
    manager.load_hierarchy("configs/base.yml")
    print("✓ Layer 1: base.yml (defaults)")

    # Layer 2: Environment overrides
    manager.load_hierarchy("configs/production.yml")
    print("✓ Layer 2: production.yml (env-specific)")

    # Layer 3: Runtime overrides
    manager.add_runtime_overrides({
        "llm.agents.discovery.model": "claude-3-opus-20240229",
        "system.deployment_id": "prod-deploy-789"
    })
    print("✓ Layer 3: runtime overrides (highest priority)\n")

    manager.merge()

    print("Results:")
    print(f"  Discovery model: {manager.get_value('llm.agents.discovery.model')}")
    print(f"  (Runtime override wins)")
    print(f"  Environment: {manager.get_value('system.environment')}")
    print(f"  (Production config wins)")
    print(f"  System name: {manager.get_value('system.name')}")
    print(f"  (Base config - no override)\n")


def demo_custom_uri_resolver():
    """
    Demonstrate custom URI resolver for environment variables
    """
    print("=== Custom URI Resolver Demo ===\n")

    # Define custom resolver for env:// URIs
    def resolve_env_uri(uri_ref: URIReference) -> str:
        """Resolve env:// URIs to environment variables"""
        import os
        var_name = uri_ref.uri.replace("env://", "")
        value = os.environ.get(var_name)
        if value is None:
            return f"[Environment variable {var_name} not set]"
        return value

    manager = ConfigManager()

    # Register custom resolver
    manager.register_uri_resolver("env", resolve_env_uri)
    print("✓ Registered custom resolver for env:// URIs")

    # Create config with env:// references
    config_yaml = """
api:
  anthropic_key: "env://ANTHROPIC_API_KEY"
  openai_key: "env://OPENAI_API_KEY"

database:
  connection_string: "env://DATABASE_URL"
"""

    manager.load_hierarchy_from_string(config_yaml, "env_config")
    manager.merge()

    print("\nResolving environment variable URIs:")
    print(f"  Anthropic Key: {manager.get_content('api.anthropic_key')}")
    print(f"  OpenAI Key: {manager.get_content('api.openai_key')}")
    print(f"  Database URL: {manager.get_content('database.connection_string')}\n")


def demo_merge_strategies():
    """
    Compare different merge strategies
    """
    print("=== Merge Strategy Comparison ===\n")

    base_yaml = """
agent:
  model: "claude-3-opus"
  temperature: 0
  prompt: "file://prompts/base.txt"
"""

    override_yaml = """
agent:
  model: "gpt-4o"
  max_tokens: 4000
"""

    # Strategy 1: OVERRIDE (default - later wins)
    print("1. OVERRIDE strategy (later wins):")
    manager = ConfigManager(merge_strategy=MergeStrategy.OVERRIDE)
    manager.load_hierarchy_from_string(base_yaml, "base")
    manager.load_hierarchy_from_string(override_yaml, "override")
    manager.merge()
    print(f"   Model: {manager.get_value('agent.model')} (override wins)")
    print(f"   Temperature: {manager.get_value('agent.temperature')} (preserved from base)")
    print(f"   Max tokens: {manager.get_value('agent.max_tokens')} (added by override)")

    # Strategy 2: URI_PRIORITY (URIs have priority)
    print("\n2. URI_PRIORITY strategy (URIs preferred):")
    manager2 = ConfigManager(merge_strategy=MergeStrategy.URI_PRIORITY)
    manager2.load_hierarchy_from_string(base_yaml, "base")
    manager2.load_hierarchy_from_string(override_yaml, "override")
    manager2.merge()
    uri = manager2.get_uri('agent.prompt')
    print(f"   Prompt URI preserved: {uri}")
    print(f"   (URI references protected from override)\n")


def demo_comparison_with_c4h():
    """
    Show how this is similar to C4H but more generic
    """
    print("=== Comparison with C4H ===\n")

    print("C4H approach (embedded YAML):")
    print("""
  agents:
    discovery:
      prompts:
        system: |
          You are a discovery agent...
          [100 lines of embedded text]
""")

    print("\nAI_SDLC_Context approach (URI references):")
    print("""
  agents:
    discovery:
      prompts:
        system: "file://prompts/discovery.md"
        # or: "https://docs.company.com/prompts/discovery"
""")

    print("\nAdvantages:")
    print("  ✓ Content lives at any URI (file, web, S3, etc.)")
    print("  ✓ Configuration stays small and readable")
    print("  ✓ Content can be versioned separately")
    print("  ✓ Easy to update prompts without redeploying")
    print("  ✓ Generic - works with any content type\n")


def main():
    print("╔════════════════════════════════════════════════╗")
    print("║  AI_SDLC_Context Advanced Usage Examples       ║")
    print("╚════════════════════════════════════════════════╝\n")

    demo_three_layer_merge()
    print("\n" + "=" * 60 + "\n")

    demo_custom_uri_resolver()
    print("\n" + "=" * 60 + "\n")

    demo_merge_strategies()
    print("\n" + "=" * 60 + "\n")

    demo_comparison_with_c4h()

    print("✅ All demos complete!")


if __name__ == "__main__":
    main()
