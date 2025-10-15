#!/usr/bin/env python3
"""
Example: Dynamic Merge Tuple Definition

This demonstrates how to dynamically define merge tuples at runtime
using the MCP service, without pre-configuring base_projects in project.json.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository


def main():
    """Demonstrate dynamic tuple composition."""
    print("=" * 80)
    print("DYNAMIC MERGE TUPLE DEFINITION")
    print("=" * 80)
    print()

    # Initialize repository
    repo_path = Path(__file__).parent.parent / "example_projects_repo"
    repo = ProjectRepository(root_path=repo_path)

    print("📋 Scenario: Create different environment configs dynamically")
    print()

    # ==========================================================================
    # Example 1: Development Environment
    # ==========================================================================
    print("=" * 80)
    print("Example 1: Development Environment (Relaxed Requirements)")
    print("=" * 80)
    print()

    print("Dynamic tuple:")
    print("  ai_init_methodology → python_standards → payment_gateway")
    print()
    print("Runtime overrides:")
    print("  • environment: development")
    print("  • testing.min_coverage: 80  (relaxed from 95)")
    print("  • debug: True")
    print()

    dev_config = repo.merge_projects(
        source_projects=[
            "ai_init_methodology",    # Sacred Seven baseline
            "python_standards",        # Python-specific standards
            "payment_gateway"          # Payment requirements
        ],
        target_name=f"payment_dev_{datetime.now().strftime('%Y%m%d_%H%M')}",
        runtime_overrides={
            "environment": "development",
            "debug": True,
            "methodology": {
                "testing": {
                    "min_coverage": 80
                }
            },
            "security": {
                "vulnerability_management": {
                    "scan_frequency": "daily"
                }
            }
        },
        description="Development environment with relaxed requirements"
    )

    print(f"✓ Created: {dev_config.name}")
    print(f"  Type: {dev_config.project_type}")
    print(f"  Merged from: {', '.join(dev_config.merged_from)}")
    print(f"  Runtime overrides: {len(dev_config.runtime_overrides)} keys")
    print()

    # ==========================================================================
    # Example 2: Staging Environment
    # ==========================================================================
    print("=" * 80)
    print("Example 2: Staging Environment (Moderate Requirements)")
    print("=" * 80)
    print()

    print("Same tuple, different overrides:")
    print("  ai_init_methodology → python_standards → payment_gateway")
    print()
    print("Runtime overrides:")
    print("  • environment: staging")
    print("  • testing.min_coverage: 90")
    print("  • auto_deploy: True")
    print()

    staging_config = repo.merge_projects(
        source_projects=[
            "ai_init_methodology",
            "python_standards",
            "payment_gateway"
        ],
        target_name=f"payment_staging_{datetime.now().strftime('%Y%m%d_%H%M')}",
        runtime_overrides={
            "environment": "staging",
            "methodology": {
                "testing": {
                    "min_coverage": 90
                }
            },
            "deployment": {
                "auto_deploy": True,
                "approval_chain": ["tech_lead"]
            },
            "monitoring": {
                "verbose_logging": True
            }
        },
        description="Staging environment with moderate requirements"
    )

    print(f"✓ Created: {staging_config.name}")
    print(f"  Merged from: {', '.join(staging_config.merged_from)}")
    print()

    # ==========================================================================
    # Example 3: Production Environment
    # ==========================================================================
    print("=" * 80)
    print("Example 3: Production Environment (Strict Requirements)")
    print("=" * 80)
    print()

    print("Same tuple, strictest overrides:")
    print("  ai_init_methodology → python_standards → payment_gateway")
    print()
    print("Runtime overrides:")
    print("  • environment: production")
    print("  • testing.min_coverage: 99  (stricter than default 95)")
    print("  • security.scan_frequency: continuous")
    print()

    prod_config = repo.merge_projects(
        source_projects=[
            "ai_init_methodology",
            "python_standards",
            "payment_gateway"
        ],
        target_name=f"payment_prod_{datetime.now().strftime('%Y%m%d_%H%M')}",
        runtime_overrides={
            "environment": "production",
            "methodology": {
                "testing": {
                    "min_coverage": 99
                }
            },
            "security": {
                "vulnerability_management": {
                    "scan_frequency": "continuous",
                    "critical_fix_sla_hours": 2
                }
            },
            "deployment": {
                "auto_deploy": False,
                "approval_chain": ["tech_lead", "security_lead", "cto"]
            },
            "build": {
                "version": "2.1.0",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "environment": "production"
            }
        },
        description="Production environment with maximum security"
    )

    print(f"✓ Created: {prod_config.name}")
    print(f"  Merged from: {', '.join(prod_config.merged_from)}")
    print()

    # ==========================================================================
    # Example 4: Custom Tuple (Different Projects)
    # ==========================================================================
    print("=" * 80)
    print("Example 4: Custom Tuple (Different Base Projects)")
    print("=" * 80)
    print()

    print("Custom tuple:")
    print("  ai_init_methodology → security_baseline → payment_gateway")
    print("  (Note: Using different middle layer)")
    print()

    # This would work if security_baseline existed
    # custom_config = repo.merge_projects(
    #     source_projects=[
    #         "ai_init_methodology",
    #         "security_baseline",      # Different middle layer!
    #         "payment_gateway"
    #     ],
    #     target_name="payment_ultra_secure",
    #     runtime_overrides={
    #         "security.level": "maximum"
    #     }
    # )

    print("(Skipped - security_baseline project would need to exist)")
    print()

    # ==========================================================================
    # Example 5: Verify Different Configurations
    # ==========================================================================
    print("=" * 80)
    print("Example 5: Verify Configurations Are Different")
    print("=" * 80)
    print()

    print("Loading and comparing configurations...")
    print()

    # Load dev config
    dev_manager = repo.get_project_config(dev_config.name)
    dev_coverage = dev_manager.get_value("methodology.testing.min_coverage")
    dev_env = dev_manager.get_value("environment")

    print(f"Development config:")
    print(f"  • Coverage: {dev_coverage}%")
    print(f"  • Environment: {dev_env}")
    print()

    # Load staging config
    staging_manager = repo.get_project_config(staging_config.name)
    staging_coverage = staging_manager.get_value("methodology.testing.min_coverage")
    staging_env = staging_manager.get_value("environment")

    print(f"Staging config:")
    print(f"  • Coverage: {staging_coverage}%")
    print(f"  • Environment: {staging_env}")
    print()

    # Load prod config
    prod_manager = repo.get_project_config(prod_config.name)
    prod_coverage = prod_manager.get_value("methodology.testing.min_coverage")
    prod_env = prod_manager.get_value("environment")

    print(f"Production config:")
    print(f"  • Coverage: {prod_coverage}%")
    print(f"  • Environment: {prod_env}")
    print()

    print("✓ Same tuple, different runtime overrides = different configs!")
    print()

    # ==========================================================================
    # Summary
    # ==========================================================================
    print("=" * 80)
    print("SUMMARY: Dynamic Tuple Benefits")
    print("=" * 80)
    print()

    print("✅ Dynamic Composition:")
    print("   • Specify tuple at runtime (not in project.json)")
    print("   • Any combination of projects")
    print("   • Any order")
    print()

    print("✅ Runtime Overrides:")
    print("   • Highest priority (override everything)")
    print("   • Environment-specific values")
    print("   • Feature flags")
    print("   • Build metadata")
    print()

    print("✅ Use Cases:")
    print("   • CI/CD pipelines (per branch/environment)")
    print("   • A/B testing (feature flags)")
    print("   • Team-specific configs")
    print("   • Time-based configs (deployment snapshots)")
    print()

    print("✅ Provenance:")
    print("   • Every merged config records:")
    print("     - Which projects were merged")
    print("     - When it was created")
    print("     - What overrides were applied")
    print()

    print("=" * 80)
    print("✓ Example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
