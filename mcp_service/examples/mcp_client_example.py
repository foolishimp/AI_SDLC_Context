#!/usr/bin/env python3
"""
Example MCP client demonstrating ai_sdlc_method service usage.

This example shows how to:
1. Create projects via MCP
2. Update project configurations
3. Merge projects
4. Inspect projects using LLM

Note: This requires the MCP server to be running.
"""
import asyncio
import json
from pathlib import Path

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp")
    exit(1)


async def run_example():
    """Run the MCP client example."""

    # Server parameters - points to our MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "server.main"],
        cwd=str(Path(__file__).parent.parent)
    )

    print("=" * 80)
    print("AI_SDLC_CONFIG MCP SERVICE EXAMPLE")
    print("=" * 80)
    print()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            print("✓ Connected to MCP server\n")

            # Example 1: Create a corporate base project
            print("=" * 80)
            print("EXAMPLE 1: Create Corporate Base Project")
            print("=" * 80)

            result = await session.call_tool(
                "create_project",
                arguments={
                    "name": "corporate_base",
                    "type": "base",
                    "base_projects": [],
                    "config": {
                        "corporate": {
                            "policies": {
                                "security": {
                                    "uri": "file://docs/policies/security.md",
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
                                "min_coverage": 80
                            },
                            "coding": {
                                "max_complexity": 10
                            }
                        }
                    },
                    "description": "Corporate-wide policies and standards"
                }
            )

            print("Created project:")
            for content in result.content:
                print(content.text)
            print()

            # Example 2: Create a Python methodology project
            print("=" * 80)
            print("EXAMPLE 2: Create Python Methodology Project")
            print("=" * 80)

            result = await session.call_tool(
                "create_project",
                arguments={
                    "name": "python_methodology",
                    "type": "methodology",
                    "base_projects": ["corporate_base"],
                    "config": {
                        "methodology": {
                            "coding": {
                                "standards": {
                                    "style_guide": "PEP 8"
                                }
                            },
                            "testing": {
                                "framework": "pytest",
                                "plugins": ["pytest-cov", "pytest-mock"]
                            }
                        }
                    },
                    "description": "Python-specific standards and tools"
                }
            )

            print("Created project:")
            for content in result.content:
                print(content.text)
            print()

            # Example 3: Create a payment service project
            print("=" * 80)
            print("EXAMPLE 3: Create Payment Service Project")
            print("=" * 80)

            result = await session.call_tool(
                "create_project",
                arguments={
                    "name": "payment_service",
                    "type": "custom",
                    "base_projects": ["corporate_base", "python_methodology"],
                    "config": {
                        "project": {
                            "name": "Payment Service",
                            "team": "Payments Team",
                            "classification": "restricted",
                            "pci_compliant": True
                        },
                        "methodology": {
                            "testing": {
                                "min_coverage": 95  # Stricter than corporate
                            }
                        },
                        "security": {
                            "vulnerability_management": {
                                "critical_fix_sla_hours": 4
                            }
                        }
                    },
                    "description": "Payment processing microservice"
                }
            )

            print("Created project:")
            for content in result.content:
                print(content.text)
            print()

            # Example 4: Add a document to the project
            print("=" * 80)
            print("EXAMPLE 4: Add Documentation")
            print("=" * 80)

            result = await session.call_tool(
                "add_document",
                arguments={
                    "project": "payment_service",
                    "path": "architecture/pci_compliance.md",
                    "content": """# PCI Compliance Requirements

## Overview
This document outlines PCI DSS compliance requirements for the Payment Service.

## Requirements
- SAQ D certification required
- Annual PCI audit
- Quarterly vulnerability scans
- Network segmentation
- Encryption at rest and in transit
- Access logging and monitoring

## Responsibilities
- Tech Lead: Architecture compliance
- Security Team: Audits and scans
- Compliance: Certification
"""
                }
            )

            print("Added document:")
            for content in result.content:
                print(content.text)
            print()

            # Example 5: Update project configuration
            print("=" * 80)
            print("EXAMPLE 5: Update Project Configuration")
            print("=" * 80)

            result = await session.call_tool(
                "update_project",
                arguments={
                    "name": "payment_service",
                    "updates": {
                        "methodology.deployment.approval_chain.production": [
                            "tech_lead",
                            "qa_lead",
                            "security_lead",
                            "compliance_officer",
                            "cto"
                        ]
                    }
                }
            )

            print("Updated project:")
            for content in result.content:
                print(content.text)
            print()

            # Example 6: List all projects
            print("=" * 80)
            print("EXAMPLE 6: List All Projects")
            print("=" * 80)

            result = await session.call_tool("list_projects", arguments={})

            print("Projects in repository:")
            for content in result.content:
                projects = json.loads(content.text)
                for project in projects:
                    print(f"  • {project['name']} ({project['type']})")
                    print(f"    Base: {', '.join(project['base_projects']) or 'None'}")
                    print(f"    Description: {project['description']}")
                    print()

            # Example 7: Merge projects for production
            print("=" * 80)
            print("EXAMPLE 7: Merge Projects for Production Deployment")
            print("=" * 80)

            result = await session.call_tool(
                "merge_projects",
                arguments={
                    "source_projects": [
                        "corporate_base",
                        "python_methodology",
                        "payment_service"
                    ],
                    "target_project": "payment_service_production",
                    "runtime_overrides": {
                        "environment": "production",
                        "security.vulnerability_management.scan_frequency": "continuous"
                    },
                    "description": "Production deployment configuration for Payment Service"
                }
            )

            print("Merged project created:")
            for content in result.content:
                data = json.loads(content.text)
                print(f"  Name: {data['name']}")
                print(f"  Type: {data['project_type']}")
                print(f"  Merged from: {', '.join(data['merged_from'])}")
                print(f"  Merge date: {data['merge_date']}")
                print(f"  Runtime overrides: {json.dumps(data['runtime_overrides'], indent=4)}")
            print()

            # Example 8: Inspect a project (LLM-powered)
            print("=" * 80)
            print("EXAMPLE 8: Inspect Project with LLM")
            print("=" * 80)

            result = await session.call_tool(
                "inspect_project",
                arguments={
                    "project": "payment_service",
                    "query": "What are the testing requirements and security SLAs?"
                }
            )

            print("Inspection result:")
            for content in result.content:
                print(content.text)
            print()

            # Example 9: Compare projects
            print("=" * 80)
            print("EXAMPLE 9: Compare Projects")
            print("=" * 80)

            # First create an internal dashboard for comparison
            await session.call_tool(
                "create_project",
                arguments={
                    "name": "internal_dashboard",
                    "type": "custom",
                    "base_projects": ["corporate_base", "python_methodology"],
                    "config": {
                        "project": {
                            "name": "Internal Dashboard",
                            "team": "Tools Team",
                            "classification": "internal"
                        },
                        "methodology": {
                            "testing": {
                                "min_coverage": 75  # More relaxed
                            }
                        }
                    },
                    "description": "Internal developer dashboard"
                }
            )

            result = await session.call_tool(
                "compare_projects",
                arguments={
                    "project1": "payment_service",
                    "project2": "internal_dashboard",
                    "query": "Compare testing requirements and security standards"
                }
            )

            print("Comparison result:")
            for content in result.content:
                print(content.text[:1000])  # First 1000 chars
            print("\n... (output truncated)")
            print()

            # Example 10: Demonstrate custom override vs merged project
            print("=" * 80)
            print("EXAMPLE 10: Custom Override vs Merged Project")
            print("=" * 80)

            print("Custom Override Project (payment_service):")
            print("  - Manually created YAML configuration")
            print("  - Inherits from base projects at runtime")
            print("  - Configuration is explicit overrides")
            print()

            result = await session.call_tool(
                "get_project",
                arguments={"name": "payment_service"}
            )

            for content in result.content:
                data = json.loads(content.text)
                print(f"  Type: {data['project_type']}")
                print(f"  Base Projects: {', '.join(data['base_projects'])}")
                print(f"  Merged From: {data.get('merged_from', 'N/A')}")
                print()

            print("Merged Project (payment_service_production):")
            print("  - Auto-generated from merge operation")
            print("  - Contains full merged configuration")
            print("  - Includes merge metadata (sources, date, overrides)")
            print("  - Immutable snapshot for deployment")
            print()

            result = await session.call_tool(
                "get_project",
                arguments={"name": "payment_service_production"}
            )

            for content in result.content:
                data = json.loads(content.text)
                print(f"  Type: {data['project_type']}")
                print(f"  Base Projects: {', '.join(data['base_projects'])}")
                print(f"  Merged From: {', '.join(data['merged_from'])}")
                print(f"  Merge Date: {data['merge_date']}")
                print(f"  Runtime Overrides: {json.dumps(data['runtime_overrides'], indent=4)}")
                print()

            print("=" * 80)
            print("✓ Example completed successfully!")
            print("=" * 80)
            print()
            print("Key Takeaways:")
            print("  • Projects are stored in git-backed repository")
            print("  • CRUD operations modify and commit changes")
            print("  • Merge creates new immutable project snapshots")
            print("  • Custom overrides vs merged projects are clearly distinguished")
            print("  • LLM inspection enables natural language queries")
            print("  • Perfect for CI/CD pipelines and deployment workflows")
            print()


if __name__ == "__main__":
    asyncio.run(run_example())
