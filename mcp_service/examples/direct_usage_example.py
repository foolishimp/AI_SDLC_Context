#!/usr/bin/env python3
"""
Direct usage example of the ProjectRepository (without MCP protocol).

This demonstrates using the storage layer directly for testing or
integration into other systems.
"""
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository


def main():
    """Run the direct usage example."""

    # Create temporary repository for demo
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Using temporary repository: {temp_dir}\n")

    try:
        # Initialize repository
        repo = ProjectRepository(temp_dir)
        print("✓ Repository initialized\n")

        print("=" * 80)
        print("EXAMPLE 1: Create Base Projects")
        print("=" * 80)

        # Create corporate base
        corporate = repo.create_project(
            name="corporate_base",
            project_type="base",
            base_projects=[],
            config={
                "corporate": {
                    "policies": {
                        "security": {
                            "uri": "file://docs/policies/security.md",
                            "version": "2.0",
                            "mandatory": True
                        }
                    }
                },
                "methodology": {
                    "testing": {
                        "min_coverage": 80
                    }
                }
            },
            description="Corporate policies and standards"
        )

        print(f"Created: {corporate.name} (type: {corporate.project_type})")
        print(f"  Version: {corporate.version}")
        print(f"  Created: {corporate.created}")
        print()

        # Create Python methodology
        python_method = repo.create_project(
            name="python_methodology",
            project_type="methodology",
            base_projects=["corporate_base"],
            config={
                "methodology": {
                    "coding": {
                        "standards": {
                            "style_guide": "PEP 8",
                            "max_function_lines": 50
                        }
                    },
                    "testing": {
                        "framework": "pytest"
                    }
                }
            },
            description="Python-specific standards"
        )

        print(f"Created: {python_method.name} (type: {python_method.project_type})")
        print(f"  Base projects: {', '.join(python_method.base_projects)}")
        print()

        print("=" * 80)
        print("EXAMPLE 2: Create Custom Project with Overrides")
        print("=" * 80)

        # Create payment service (custom overrides)
        payment = repo.create_project(
            name="payment_service",
            project_type="custom",
            base_projects=["corporate_base", "python_methodology"],
            config={
                "project": {
                    "name": "Payment Service",
                    "team": "Payments Team",
                    "pci_compliant": True
                },
                "methodology": {
                    "testing": {
                        "min_coverage": 95  # Override corporate 80%
                    }
                },
                "security": {
                    "vulnerability_management": {
                        "critical_fix_sla_hours": 4  # Stricter than default
                    }
                }
            },
            description="Payment processing microservice"
        )

        print(f"Created: {payment.name} (type: {payment.project_type})")
        print(f"  Base projects: {', '.join(payment.base_projects)}")
        print(f"  Description: {payment.description}")
        print()

        print("=" * 80)
        print("EXAMPLE 3: Add Documentation")
        print("=" * 80)

        doc_path = repo.add_document(
            project_name="payment_service",
            doc_path="architecture/overview.md",
            content="""# Payment Service Architecture

## Overview
Microservice for processing payments securely.

## Components
- API Gateway
- Payment Processor
- Fraud Detection
- Audit Logger

## Security
- PCI DSS compliant
- End-to-end encryption
- Token-based authentication
"""
        )

        print(f"Added document: {doc_path}")
        print()

        print("=" * 80)
        print("EXAMPLE 4: Update Configuration")
        print("=" * 80)

        updated = repo.update_project(
            name="payment_service",
            updates={
                "methodology.deployment.approval_chain.production": [
                    "tech_lead", "qa_lead", "security_lead", "cto"
                ],
                "quality.gates.max_critical_issues": 0
            }
        )

        print(f"Updated: {updated.name}")
        print(f"  Modified: {updated.modified}")
        print()

        print("=" * 80)
        print("EXAMPLE 5: Merge Projects for Production")
        print("=" * 80)

        merged = repo.merge_projects(
            source_projects=[
                "corporate_base",
                "python_methodology",
                "payment_service"
            ],
            target_name="payment_service_production",
            runtime_overrides={
                "environment": "production",
                "security.vulnerability_management.scan_frequency": "continuous"
            },
            description="Production configuration for Payment Service"
        )

        print(f"Created merged project: {merged.name}")
        print(f"  Type: {merged.project_type}")
        print(f"  Merged from: {', '.join(merged.merged_from)}")
        print(f"  Merge date: {merged.merge_date}")
        print(f"  Runtime overrides: {merged.runtime_overrides}")
        print()

        print("=" * 80)
        print("EXAMPLE 6: Access Merged Configuration")
        print("=" * 80)

        # Get config manager for merged project
        config = repo.get_project_config("payment_service_production")

        # Access specific values
        min_coverage = config.get_value("methodology.testing.min_coverage")
        scan_freq = config.get_value("security.vulnerability_management.scan_frequency")
        environment = config.get_value("environment")

        print(f"Merged configuration values:")
        print(f"  Min coverage: {min_coverage}%")
        print(f"  Scan frequency: {scan_freq}")
        print(f"  Environment: {environment}")
        print()

        print("=" * 80)
        print("EXAMPLE 7: List All Projects")
        print("=" * 80)

        projects = repo.list_projects()
        print(f"Total projects: {len(projects)}\n")

        for proj in projects:
            print(f"  • {proj.name} ({proj.project_type})")
            print(f"    Base: {', '.join(proj.base_projects) or 'None'}")
            if proj.merged_from:
                print(f"    Merged from: {', '.join(proj.merged_from)}")
            print()

        print("=" * 80)
        print("KEY DISTINCTION: Custom vs Merged Projects")
        print("=" * 80)

        payment_meta = repo.get_project(("payment_service"))
        merged_meta = repo.get_project("payment_service_production")

        print("Custom Override Project (payment_service):")
        print(f"  Type: {payment_meta.project_type}")
        print(f"  Purpose: Manual configuration with explicit overrides")
        print(f"  Storage: config/config.yml (contains only overrides)")
        print(f"  Merged from: {payment_meta.merged_from or 'N/A'}")
        print(f"  Use case: Active development, living configuration")
        print()

        print("Merged Project (payment_service_production):")
        print(f"  Type: {merged_meta.project_type}")
        print(f"  Purpose: Immutable deployment snapshot")
        print(f"  Storage: config/merged.yml (contains full merged config)")
        print(f"  Merged from: {', '.join(merged_meta.merged_from)}")
        print(f"  Merge date: {merged_meta.merge_date}")
        print(f"  Runtime overrides: {merged_meta.runtime_overrides}")
        print(f"  Use case: CI/CD deployment, reproducible builds")
        print()

        print("=" * 80)
        print("✓ Example completed successfully!")
        print("=" * 80)
        print()
        print("Benefits demonstrated:")
        print("  ✓ Git-backed storage with automatic commits")
        print("  ✓ Project inheritance and layering")
        print("  ✓ Clear distinction between custom and merged projects")
        print("  ✓ Merge creates immutable snapshots")
        print("  ✓ Runtime overrides applied during merge")
        print("  ✓ Full audit trail via git history")
        print()

    finally:
        # Cleanup
        print(f"Cleaning up temporary repository: {temp_dir}")
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
