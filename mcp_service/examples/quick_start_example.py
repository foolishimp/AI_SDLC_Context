#!/usr/bin/env python3
"""
Quick Start Example - Real-world usage of AI_SDLC_Context MCP service.

This example shows a realistic scenario:
1. Setting up corporate standards
2. Adding language-specific methodologies
3. Creating project-specific configurations
4. Merging for production deployment
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_service.storage.project_repository import ProjectRepository


def main():
    """Run quick start example."""

    # Use a local projects repository (creates if doesn't exist)
    repo_path = Path.cwd() / "example_projects_repo"
    print(f"📁 Using repository: {repo_path}\n")

    repo = ProjectRepository(repo_path)

    # =============================================================================
    # STEP 1: Create corporate base with security and testing standards
    # =============================================================================
    print("=" * 80)
    print("STEP 1: Creating corporate base project")
    print("=" * 80)

    corporate = repo.create_project(
        name="acme_corporate",
        project_type="base",
        base_projects=[],
        config={
            "corporate": {
                "name": "Acme Corporation",
                "policies": {
                    "security": {
                        "uri": "file://docs/policies/security_policy.md",
                        "version": "2.0",
                        "mandatory": True
                    },
                    "code_review": {
                        "uri": "file://docs/policies/code_review.md",
                        "version": "1.0",
                        "mandatory": True
                    }
                }
            },
            "methodology": {
                "testing": {
                    "min_coverage": 80,
                    "required_types": ["unit", "integration"]
                },
                "coding": {
                    "max_function_lines": 50,
                    "max_complexity": 10
                }
            },
            "quality": {
                "gates": {
                    "code_quality": {
                        "max_critical_issues": 0,
                        "max_high_issues": 5,
                        "max_code_smells": 20
                    }
                }
            }
        },
        description="Corporate-wide policies and standards"
    )

    print(f"✓ Created: {corporate.name}")
    print(f"  Type: {corporate.project_type}")
    print(f"  Version: {corporate.version}\n")

    # =============================================================================
    # STEP 2: Create Python methodology
    # =============================================================================
    print("=" * 80)
    print("STEP 2: Creating Python methodology")
    print("=" * 80)

    python_method = repo.create_project(
        name="python_standards",
        project_type="methodology",
        base_projects=["acme_corporate"],
        config={
            "methodology": {
                "coding": {
                    "standards": {
                        "style_guide": "PEP 8",
                        "formatter": "black",
                        "type_checking": True
                    },
                    "linting": {
                        "tools": ["pylint", "flake8", "mypy", "black"]
                    }
                },
                "testing": {
                    "framework": "pytest",
                    "plugins": ["pytest-cov", "pytest-mock", "pytest-asyncio"]
                }
            },
            "tools": {
                "package_management": {
                    "tool": "poetry",
                    "python_version": "^3.9"
                }
            }
        },
        description="Python-specific coding standards and tools"
    )

    print(f"✓ Created: {python_method.name}")
    print(f"  Base projects: {', '.join(python_method.base_projects)}\n")

    # =============================================================================
    # STEP 3: Create a high-security payment service
    # =============================================================================
    print("=" * 80)
    print("STEP 3: Creating payment service with strict requirements")
    print("=" * 80)

    payment = repo.create_project(
        name="payment_gateway",
        project_type="custom",
        base_projects=["acme_corporate", "python_standards"],
        config={
            "project": {
                "name": "Payment Gateway",
                "team": "Payments Team",
                "tech_lead": "alice@acme.com",
                "classification": "restricted",
                "pci_compliant": True
            },
            "methodology": {
                "testing": {
                    "min_coverage": 95,  # Stricter than corporate 80%
                    "required_types": [
                        "unit",
                        "integration",
                        "security",
                        "penetration",
                        "load"
                    ]
                }
            },
            "security": {
                "vulnerability_management": {
                    "scan_frequency": "daily",
                    "critical_fix_sla_hours": 4,
                    "high_fix_sla_hours": 24
                },
                "compliance": {
                    "frameworks": ["PCI DSS", "SOC2", "GDPR"]
                }
            },
            "quality": {
                "gates": {
                    "code_quality": {
                        "max_critical_issues": 0,
                        "max_high_issues": 0,  # Stricter than corporate
                        "max_code_smells": 0
                    }
                }
            }
        },
        description="High-security payment processing gateway"
    )

    print(f"✓ Created: {payment.name}")
    print(f"  Classification: {repo.get_project_config('payment_gateway').get_value('project.classification')}")
    print(f"  PCI Compliant: {repo.get_project_config('payment_gateway').get_value('project.pci_compliant')}")
    print(f"  Min Coverage: {repo.get_project_config('payment_gateway').get_value('methodology.testing.min_coverage')}%\n")

    # =============================================================================
    # STEP 4: Add architecture documentation
    # =============================================================================
    print("=" * 80)
    print("STEP 4: Adding documentation")
    print("=" * 80)

    arch_doc = repo.add_document(
        project_name="payment_gateway",
        doc_path="architecture/system_design.md",
        content="""# Payment Gateway Architecture

## Overview
Microservice-based payment processing system with PCI DSS compliance.

## Components
- **API Gateway**: Rate limiting, authentication, routing
- **Payment Processor**: Transaction handling, card tokenization
- **Fraud Detection**: Real-time ML-based fraud scoring
- **Audit Logger**: Immutable transaction logs
- **Settlement Engine**: Batch processing for reconciliation

## Security
- End-to-end encryption (TLS 1.3)
- Card data tokenization (PCI DSS Level 1)
- MFA for admin access
- Network segmentation and DMZ
- Real-time security monitoring

## Compliance
- PCI DSS SAQ D certification
- SOC2 Type II audit annually
- GDPR data protection compliance
"""
    )

    print(f"✓ Added document: architecture/system_design.md\n")

    # =============================================================================
    # STEP 5: Update deployment approval chain
    # =============================================================================
    print("=" * 80)
    print("STEP 5: Configuring deployment approvals")
    print("=" * 80)

    updated = repo.update_project(
        name="payment_gateway",
        updates={
            "methodology.deployment.approval_chain.development": [
                "tech_lead"
            ],
            "methodology.deployment.approval_chain.staging": [
                "tech_lead",
                "qa_lead"
            ],
            "methodology.deployment.approval_chain.production": [
                "tech_lead",
                "qa_lead",
                "security_lead",
                "compliance_officer",
                "cto"
            ]
        }
    )

    print(f"✓ Updated deployment approval chain")
    config = repo.get_project_config("payment_gateway")
    prod_approvers = config.get_value("methodology.deployment.approval_chain.production")
    if prod_approvers:
        print(f"  Production approvers: {', '.join(prod_approvers)}\n")
    else:
        print(f"  Production approvers: [configuration needs merge]\n")

    # =============================================================================
    # STEP 6: Create an internal dashboard (lower security requirements)
    # =============================================================================
    print("=" * 80)
    print("STEP 6: Creating internal dashboard (relaxed requirements)")
    print("=" * 80)

    dashboard = repo.create_project(
        name="admin_dashboard",
        project_type="custom",
        base_projects=["acme_corporate", "python_standards"],
        config={
            "project": {
                "name": "Admin Dashboard",
                "team": "Tools Team",
                "classification": "internal"
            },
            "methodology": {
                "testing": {
                    "min_coverage": 75,  # More relaxed than corporate
                    "required_types": ["unit", "integration"]
                }
            },
            "quality": {
                "gates": {
                    "code_quality": {
                        "max_code_smells": 30  # More lenient
                    }
                }
            }
        },
        description="Internal operations dashboard"
    )

    print(f"✓ Created: {dashboard.name}")
    dash_config = repo.get_project_config("admin_dashboard")
    print(f"  Classification: {dash_config.get_value('project.classification')}")
    print(f"  Min Coverage: {dash_config.get_value('methodology.testing.min_coverage')}%\n")

    # =============================================================================
    # STEP 7: Merge payment gateway for production deployment
    # =============================================================================
    print("=" * 80)
    print("STEP 7: Merging for production deployment")
    print("=" * 80)

    merged = repo.merge_projects(
        source_projects=[
            "acme_corporate",
            "python_standards",
            "payment_gateway"
        ],
        target_name="payment_gateway_prod_v1_0_0",
        runtime_overrides={
            "environment": "production",
            "build": {
                "version": "1.0.0",
                "timestamp": "2025-10-14T16:00:00Z",
                "commit": "abc123def"
            },
            "security": {
                "vulnerability_management": {
                    "scan_frequency": "continuous"  # Override from daily
                }
            },
            "deployment": {
                "replicas": 5,
                "auto_scaling": True,
                "region": "us-east-1"
            }
        },
        description="Production deployment v1.0.0 of Payment Gateway"
    )

    print(f"✓ Created merged project: {merged.name}")
    print(f"  Type: {merged.project_type}")
    print(f"  Merged from: {', '.join(merged.merged_from)}")
    print(f"  Merge date: {merged.merge_date}")
    print(f"  Runtime overrides applied:\n")
    for key, value in merged.runtime_overrides.items():
        print(f"    • {key}: {value}")
    print()

    # =============================================================================
    # STEP 8: Access and validate merged configuration
    # =============================================================================
    print("=" * 80)
    print("STEP 8: Validating merged configuration")
    print("=" * 80)

    prod_config = repo.get_project_config("payment_gateway_prod_v1_0_0")

    # Validation checks
    print("Configuration validation:")
    print(f"  ✓ Environment: {prod_config.get_value('environment')}")
    print(f"  ✓ Build version: {prod_config.get_value('build.version')}")
    print(f"  ✓ Min coverage: {prod_config.get_value('methodology.testing.min_coverage')}%")
    print(f"  ✓ Security scan: {prod_config.get_value('security.vulnerability_management.scan_frequency')}")
    print(f"  ✓ Critical SLA: {prod_config.get_value('security.vulnerability_management.critical_fix_sla_hours')} hours")
    print(f"  ✓ Deployment replicas: {prod_config.get_value('deployment.replicas')}")
    print(f"  ✓ Auto scaling: {prod_config.get_value('deployment.auto_scaling')}")
    print()

    # =============================================================================
    # STEP 9: Compare projects
    # =============================================================================
    print("=" * 80)
    print("STEP 9: Comparing payment gateway vs admin dashboard")
    print("=" * 80)

    payment_config = repo.get_project_config("payment_gateway")
    dash_config = repo.get_project_config("admin_dashboard")

    comparisons = [
        ("Classification", "project.classification"),
        ("Min Coverage", "methodology.testing.min_coverage"),
        ("Max Code Smells", "quality.gates.code_quality.max_code_smells"),
    ]

    print(f"\n{'Metric':<25} {'Payment Gateway':<20} {'Admin Dashboard':<20}")
    print("-" * 70)
    for label, path in comparisons:
        payment_val = payment_config.get_value(path)
        dash_val = dash_config.get_value(path)
        print(f"{label:<25} {str(payment_val):<20} {str(dash_val):<20}")

    print("\n💡 Key Insight:")
    print("   Payment Gateway has STRICTER requirements (PCI compliance, financial data)")
    print("   Admin Dashboard has RELAXED requirements (internal tool, lower risk)\n")

    # =============================================================================
    # STEP 10: View git history
    # =============================================================================
    print("=" * 80)
    print("STEP 10: Git audit trail")
    print("=" * 80)

    import subprocess
    result = subprocess.run(
        ["git", "log", "--oneline", "-n", "10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    print("Recent commits (audit trail):")
    for line in result.stdout.strip().split('\n'):
        print(f"  {line}")
    print()

    # =============================================================================
    # DONE
    # =============================================================================
    print("=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print()
    print("What you just saw:")
    print("  1. ✓ Created corporate base with company-wide standards")
    print("  2. ✓ Added Python methodology (language-specific)")
    print("  3. ✓ Created payment gateway with strict PCI requirements")
    print("  4. ✓ Added architecture documentation")
    print("  5. ✓ Configured deployment approval chains")
    print("  6. ✓ Created admin dashboard with relaxed requirements")
    print("  7. ✓ Merged for production with runtime overrides")
    print("  8. ✓ Validated merged configuration")
    print("  9. ✓ Compared different project requirements")
    print(" 10. ✓ Viewed git audit trail")
    print()
    print("🎯 Key Takeaways:")
    print("  • Projects inherit from base + methodology layers")
    print("  • Each project can override defaults based on risk level")
    print("  • Merge creates immutable snapshots for deployment")
    print("  • Runtime overrides applied at merge time (env, version, etc)")
    print("  • Full git history provides audit trail")
    print("  • Custom projects vs Merged projects serve different purposes")
    print()
    print(f"📁 Repository location: {repo_path}")
    print(f"   Total projects: {len(repo.list_projects())}")
    print()


if __name__ == "__main__":
    main()
