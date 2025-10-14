"""
Enhanced MCP tools for dynamic context management.

These tools enable Claude to load, switch, and query project contexts dynamically.
"""
from typing import Dict, Any, List, Optional
from pathlib import Path


class ContextManager:
    """
    Manages Claude's current project context.

    Allows Claude to:
    - Load project contexts into working memory
    - Switch between different project contexts
    - Query current context
    - Stack multiple contexts
    """

    def __init__(self, repository):
        """
        Initialize context manager.

        Args:
            repository: ProjectRepository instance
        """
        self.repo = repository
        self.context_stack: List[Dict[str, Any]] = []
        self.current_context: Optional[Dict[str, Any]] = None

    def load_context(self, project_name: str) -> Dict[str, Any]:
        """
        Load full project context for Claude.

        This provides Claude with:
        - Project metadata and classification
        - All configuration values (merged from base projects)
        - Referenced documentation content
        - Policy requirements
        - Quality gates and standards
        - Deployment requirements

        Args:
            project_name: Name of project to load

        Returns:
            Complete project context dictionary

        Raises:
            ValueError: If project doesn't exist
        """
        # Get project metadata
        metadata = self.repo.get_project(project_name)
        if not metadata:
            raise ValueError(f"Project '{project_name}' not found")

        # Get merged configuration
        config = self.repo.get_project_config(project_name)

        # Build comprehensive context
        context = {
            "metadata": {
                "name": metadata.name,
                "type": metadata.project_type,
                "version": metadata.version,
                "base_projects": metadata.base_projects,
                "description": metadata.description
            },
            "project": {
                "name": config.get_value("project.name"),
                "team": config.get_value("project.team"),
                "tech_lead": config.get_value("project.tech_lead"),
                "classification": config.get_value("project.classification"),
                "pci_compliant": config.get_value("project.pci_compliant")
            },
            "requirements": {
                "testing": {
                    "min_coverage": config.get_value("methodology.testing.min_coverage"),
                    "required_types": config.get_value("methodology.testing.required_types"),
                    "framework": config.get_value("methodology.testing.framework")
                },
                "coding": {
                    "style_guide": config.get_value("methodology.coding.standards.style_guide"),
                    "max_function_lines": config.get_value("methodology.coding.max_function_lines"),
                    "max_complexity": config.get_value("methodology.coding.max_complexity"),
                    "linting_tools": config.get_value("methodology.coding.linting.tools")
                }
            },
            "security": {
                "vulnerability_management": config.get_value("security.vulnerability_management"),
                "compliance_frameworks": config.get_value("security.compliance.frameworks")
            },
            "quality": {
                "gates": config.get_value("quality.gates.code_quality")
            },
            "deployment": {
                "approval_chain": config.get_value("methodology.deployment.approval_chain")
            },
            "policies": self._load_policies(config),
            "documentation": self._load_documentation(config, project_name),
            "environment": config.get_value("environment"),
            "build": config.get_value("build")
        }

        # If merged project, include merge metadata
        if metadata.project_type == "merged":
            context["merge_info"] = {
                "merged_from": metadata.merged_from,
                "merge_date": metadata.merge_date,
                "runtime_overrides": metadata.runtime_overrides
            }

        self.current_context = context
        return context

    def _load_policies(self, config) -> Dict[str, Any]:
        """Load policy documents from URIs."""
        policies = {}

        # Find all policy URIs
        policy_nodes = config.find_all("corporate.policies.*")

        for path, node in policy_nodes:
            policy_name = path.split(".")[-1]
            uri = node.get_value_by_path("uri")

            if uri:
                try:
                    # Load policy content
                    content = config.get_content(path)
                    policies[policy_name] = {
                        "uri": uri,
                        "version": node.get_value_by_path("version"),
                        "mandatory": node.get_value_by_path("mandatory"),
                        "content_preview": content[:500] if content else None  # First 500 chars
                    }
                except Exception as e:
                    policies[policy_name] = {
                        "uri": uri,
                        "error": str(e)
                    }

        return policies

    def _load_documentation(self, config, project_name: str) -> Dict[str, Any]:
        """Load project documentation."""
        docs = {}

        # Find project-specific docs
        doc_nodes = config.find_all(f"projects.{project_name.replace('-', '_')}.docs.*")

        for path, node in doc_nodes:
            doc_name = path.split(".")[-1]
            uri = config.get_uri(path)

            if uri:
                try:
                    content = config.get_content(path)
                    docs[doc_name] = {
                        "uri": uri,
                        "content_preview": content[:500] if content else None
                    }
                except Exception as e:
                    docs[doc_name] = {
                        "uri": uri,
                        "error": str(e)
                    }

        return docs

    def switch_context(
        self,
        from_project: Optional[str],
        to_project: str
    ) -> Dict[str, Any]:
        """
        Switch from one project context to another.

        Shows what changed so Claude knows how to adjust its behavior.

        Args:
            from_project: Current project (None if no context loaded)
            to_project: Target project to switch to

        Returns:
            Context switch summary with requirement changes
        """
        # Load new context
        new_context = self.load_context(to_project)

        if not from_project:
            return {
                "action": "loaded",
                "project": to_project,
                "context": new_context
            }

        # Load old context for comparison
        old_metadata = self.repo.get_project(from_project)
        old_config = self.repo.get_project_config(from_project)
        new_config = self.repo.get_project_config(to_project)

        # Compare requirements
        changes = {
            "testing": self._compare_values(
                "Testing Coverage",
                old_config.get_value("methodology.testing.min_coverage"),
                new_config.get_value("methodology.testing.min_coverage")
            ),
            "classification": self._compare_values(
                "Classification",
                old_config.get_value("project.classification"),
                new_config.get_value("project.classification")
            ),
            "security_sla": self._compare_values(
                "Critical Fix SLA",
                old_config.get_value("security.vulnerability_management.critical_fix_sla_hours"),
                new_config.get_value("security.vulnerability_management.critical_fix_sla_hours")
            ),
            "max_code_smells": self._compare_values(
                "Max Code Smells",
                old_config.get_value("quality.gates.code_quality.max_code_smells"),
                new_config.get_value("quality.gates.code_quality.max_code_smells")
            )
        }

        return {
            "action": "switched",
            "from": from_project,
            "to": to_project,
            "changes": {k: v for k, v in changes.items() if v},  # Only changed values
            "new_context": new_context
        }

    def _compare_values(
        self,
        label: str,
        old_value: Any,
        new_value: Any
    ) -> Optional[Dict[str, Any]]:
        """Compare two values and return change description."""
        if old_value == new_value:
            return None

        change = {
            "label": label,
            "old": old_value,
            "new": new_value
        }

        # Add interpretation for common cases
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if new_value > old_value:
                change["direction"] = "stricter"
            else:
                change["direction"] = "relaxed"

        return change

    def push_context(self, project_name: str) -> Dict[str, Any]:
        """
        Push new context onto stack (doesn't replace current).

        Allows layering multiple contexts.

        Args:
            project_name: Project to add to stack

        Returns:
            Updated context stack
        """
        context = self.load_context(project_name)
        self.context_stack.append(context)
        return {
            "action": "pushed",
            "project": project_name,
            "stack_depth": len(self.context_stack),
            "stack": [c["metadata"]["name"] for c in self.context_stack]
        }

    def pop_context(self) -> Dict[str, Any]:
        """
        Pop context from stack.

        Returns:
            Popped context
        """
        if not self.context_stack:
            raise ValueError("Context stack is empty")

        popped = self.context_stack.pop()

        if self.context_stack:
            self.current_context = self.context_stack[-1]
        else:
            self.current_context = None

        return {
            "action": "popped",
            "project": popped["metadata"]["name"],
            "stack_depth": len(self.context_stack),
            "current": self.current_context["metadata"]["name"] if self.current_context else None
        }

    def query_context(self, question: str) -> str:
        """
        Query current context using natural language.

        Args:
            question: Natural language question about current context

        Returns:
            Answer based on current context

        Raises:
            ValueError: If no context loaded
        """
        if not self.current_context:
            raise ValueError("No context loaded. Use load_context first.")

        # Format current context for LLM
        security_info = self.current_context.get('security')
        vm_info = security_info.get('vulnerability_management') if security_info else None
        sla = vm_info.get('critical_fix_sla_hours') if vm_info else 'N/A'

        context_summary = f"""
Current Project Context: {self.current_context['metadata']['name']}

Type: {self.current_context['metadata']['type']}
Classification: {self.current_context['project'].get('classification', 'N/A')}

Requirements:
- Testing Coverage: {self.current_context['requirements']['testing']['min_coverage']}%
- Coding Style: {self.current_context['requirements']['coding'].get('style_guide', 'N/A')}
- Max Complexity: {self.current_context['requirements']['coding'].get('max_complexity', 'N/A')}

Security:
- Vulnerability SLA: {sla} hours

Quality Gates:
{self.current_context['quality'].get('gates', {})}

Environment: {self.current_context.get('environment', 'N/A')}

Question: {question}
"""

        return context_summary

    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get summary of current context.

        Returns:
            Summary of loaded context
        """
        if not self.current_context:
            return {"status": "no_context_loaded"}

        return {
            "status": "context_loaded",
            "project": self.current_context["metadata"]["name"],
            "type": self.current_context["metadata"]["type"],
            "classification": self.current_context["project"].get("classification"),
            "key_requirements": {
                "min_coverage": self.current_context["requirements"]["testing"]["min_coverage"],
                "style_guide": self.current_context["requirements"]["coding"].get("style_guide"),
                "pci_compliant": self.current_context["project"].get("pci_compliant")
            },
            "stack_depth": len(self.context_stack)
        }


# Example usage helpers

def format_context_for_llm(context: Dict[str, Any]) -> str:
    """
    Format context in a way that's easy for LLM to understand.

    Args:
        context: Project context dictionary

    Returns:
        Formatted string for LLM prompt
    """
    lines = [
        f"# Project Context: {context['metadata']['name']}",
        "",
        f"**Type**: {context['metadata']['type']}",
        f"**Classification**: {context['project'].get('classification', 'N/A')}",
        ""
    ]

    # Requirements
    lines.extend([
        "## Requirements",
        "",
        "### Testing",
        f"- Minimum Coverage: {context['requirements']['testing']['min_coverage']}%",
    ])

    # Handle required_types (might be list or dict from YAML)
    test_types = context['requirements']['testing'].get('required_types', [])
    if isinstance(test_types, list):
        lines.append(f"- Required Test Types: {', '.join(test_types)}")
    elif isinstance(test_types, dict):
        type_list = [str(v) for v in test_types.values()]
        lines.append(f"- Required Test Types: {', '.join(type_list)}")

    lines.extend([
        f"- Framework: {context['requirements']['testing'].get('framework', 'N/A')}",
        "",
        "### Coding Standards",
        f"- Style Guide: {context['requirements']['coding'].get('style_guide', 'N/A')}",
        f"- Max Function Lines: {context['requirements']['coding'].get('max_function_lines', 'N/A')}",
        f"- Max Complexity: {context['requirements']['coding'].get('max_complexity', 'N/A')}",
        ""
    ])

    # Security
    if context.get('security', {}).get('vulnerability_management'):
        vm = context['security']['vulnerability_management']
        lines.extend([
            "## Security",
            f"- Scan Frequency: {vm.get('scan_frequency', 'N/A')}",
            f"- Critical Fix SLA: {vm.get('critical_fix_sla_hours', 'N/A')} hours",
            f"- High Fix SLA: {vm.get('high_fix_sla_hours', 'N/A')} hours",
            ""
        ])

    # Policies
    if context.get('policies'):
        lines.extend(["## Policies", ""])
        for policy_name, policy_info in context['policies'].items():
            lines.append(f"- {policy_name.replace('_', ' ').title()}: {policy_info.get('uri', 'N/A')}")
        lines.append("")

    return "\n".join(lines)
