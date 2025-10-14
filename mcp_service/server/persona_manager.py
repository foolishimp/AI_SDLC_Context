"""
Persona management for role-based context customization.

Enables different team roles (BA, engineer, QA, etc.) to have customized
views and overrides of project configurations.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml


class PersonaManager:
    """
    Manages persona-based configuration overrides.

    Personas represent different team roles (business analyst, engineer, QA, etc.)
    and can customize how project configurations are presented and prioritized.
    """

    def __init__(self, personas_dir: Path):
        """
        Initialize persona manager.

        Args:
            personas_dir: Directory containing persona YAML files
        """
        self.personas_dir = Path(personas_dir)
        self.current_persona: Optional[Dict[str, Any]] = None
        self.persona_cache: Dict[str, Dict[str, Any]] = {}

    def load_persona(self, persona_name: str) -> Dict[str, Any]:
        """
        Load persona configuration.

        Args:
            persona_name: Name of persona (e.g., 'business_analyst')

        Returns:
            Persona configuration dictionary

        Raises:
            FileNotFoundError: If persona file doesn't exist
        """
        # Check cache first
        if persona_name in self.persona_cache:
            self.current_persona = self.persona_cache[persona_name]
            return self.current_persona

        # Load from file
        persona_file = self.personas_dir / f"{persona_name}.yml"
        if not persona_file.exists():
            raise FileNotFoundError(f"Persona '{persona_name}' not found at {persona_file}")

        with open(persona_file, 'r') as f:
            persona_config = yaml.safe_load(f)

        # Cache and set current
        self.persona_cache[persona_name] = persona_config
        self.current_persona = persona_config

        return persona_config

    def apply_persona_to_context(
        self,
        project_context: Dict[str, Any],
        persona_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply persona overrides to project context.

        Personas have highest priority - they override project settings.

        Args:
            project_context: Base project context
            persona_config: Persona configuration to apply

        Returns:
            Combined context with persona overrides
        """
        import copy

        # Deep copy to avoid mutating original
        combined = copy.deepcopy(project_context)

        # Add persona information
        combined['active_persona'] = {
            'name': persona_config['persona']['name'],
            'role': persona_config['persona']['role'],
            'focus_areas': persona_config['persona']['focus_areas']
        }

        # Apply persona overrides (highest priority)
        if 'overrides' in persona_config['persona']:
            overrides = persona_config['persona']['overrides']
            combined = self._deep_merge(combined, overrides)

        # Add persona preferences
        if 'preferences' in persona_config['persona']:
            combined['persona_preferences'] = persona_config['persona']['preferences']

        # Add persona tools
        if 'tools' in persona_config['persona']:
            combined['persona_tools'] = persona_config['persona']['tools']

        # Add persona documentation focus
        if 'documentation_focus' in persona_config['persona']:
            combined['persona_documentation_focus'] = persona_config['persona']['documentation_focus']

        # Add notifications
        if 'notifications' in persona_config['persona']:
            combined['persona_notifications'] = persona_config['persona']['notifications']

        return combined

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries, with override taking precedence.

        Args:
            base: Base dictionary
            override: Override dictionary (higher priority)

        Returns:
            Merged dictionary
        """
        import copy

        result = copy.deepcopy(base)

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursive merge for nested dicts
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override value
                result[key] = copy.deepcopy(value)

        return result

    def switch_persona(
        self,
        from_persona_name: Optional[str],
        to_persona_name: str
    ) -> Dict[str, Any]:
        """
        Switch from one persona to another.

        Args:
            from_persona_name: Current persona (None if no persona loaded)
            to_persona_name: Target persona

        Returns:
            Comparison showing what changed
        """
        # Load new persona
        new_persona = self.load_persona(to_persona_name)

        if not from_persona_name:
            return {
                "action": "loaded",
                "persona": to_persona_name,
                "focus_areas": new_persona['persona']['focus_areas']
            }

        # Load old persona for comparison
        old_persona_file = self.personas_dir / f"{from_persona_name}.yml"
        if old_persona_file.exists():
            with open(old_persona_file, 'r') as f:
                old_persona = yaml.safe_load(f)

            # Compare focus areas
            old_focus = old_persona['persona']['focus_areas']
            new_focus = new_persona['persona']['focus_areas']

            return {
                "action": "switched",
                "from": from_persona_name,
                "to": to_persona_name,
                "focus_changed": {
                    "old_focus": old_focus,
                    "new_focus": new_focus,
                    "added_focus": [f for f in new_focus if f not in old_focus],
                    "removed_focus": [f for f in old_focus if f not in new_focus]
                }
            }

        return {
            "action": "switched",
            "from": from_persona_name,
            "to": to_persona_name
        }

    def list_personas(self) -> List[Dict[str, str]]:
        """
        List all available personas.

        Returns:
            List of persona names and descriptions
        """
        personas = []

        for persona_file in self.personas_dir.glob("*.yml"):
            try:
                with open(persona_file, 'r') as f:
                    config = yaml.safe_load(f)

                personas.append({
                    "role": config['persona']['role'],
                    "name": config['persona']['name'],
                    "focus_areas": config['persona']['focus_areas']
                })
            except Exception as e:
                print(f"Error loading persona {persona_file}: {e}")

        return personas

    def get_persona_review_checklist(self, persona_name: Optional[str] = None) -> List[str]:
        """
        Get code review checklist for current or specified persona.

        Args:
            persona_name: Persona to get checklist for (uses current if None)

        Returns:
            List of review checklist items
        """
        persona = self.current_persona
        if persona_name:
            persona = self.load_persona(persona_name)

        if not persona:
            return []

        # Extract review checklist from overrides
        overrides = persona.get('persona', {}).get('overrides', {})
        review = overrides.get('methodology', {}).get('review', {})

        return review.get('checklist', [])

    def get_persona_preferences(self, persona_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get preferences for current or specified persona.

        Args:
            persona_name: Persona to get preferences for (uses current if None)

        Returns:
            Persona preferences dictionary
        """
        persona = self.current_persona
        if persona_name:
            persona = self.load_persona(persona_name)

        if not persona:
            return {}

        return persona.get('persona', {}).get('preferences', {})

    def format_context_for_persona(
        self,
        context: Dict[str, Any],
        persona_config: Dict[str, Any]
    ) -> str:
        """
        Format context specifically for persona's view.

        Args:
            context: Full project context
            persona_config: Persona configuration

        Returns:
            Formatted string for LLM
        """
        persona_info = persona_config['persona']
        lines = [
            f"# Context View: {persona_info['name']}",
            "",
            f"**Project**: {context['metadata']['name']}",
            f"**Role**: {persona_info['role']}",
            "",
            "## Your Focus Areas:",
        ]

        for focus in persona_info['focus_areas']:
            lines.append(f"  • {focus}")

        lines.append("")

        # Show relevant information based on persona
        prefs = persona_info.get('preferences', {})
        doc_style = prefs.get('documentation', {}).get('style', 'technical')

        if doc_style == 'narrative':
            lines.append("## Business View:")
            lines.append("(Implementation details hidden)")
        elif doc_style == 'technical':
            lines.append("## Technical View:")
            lines.append("(Full implementation details)")
        elif doc_style == 'operational':
            lines.append("## Operational View:")
            lines.append("(Deployment and infrastructure focus)")

        lines.append("")

        # Show persona-specific tools
        if 'tools' in persona_info:
            lines.append("## Your Preferred Tools:")
            for tool in persona_info['tools'].get('preferred', []):
                lines.append(f"  • {tool}")
            lines.append("")

        # Show review checklist
        overrides = persona_info.get('overrides', {})
        review_checklist = overrides.get('methodology', {}).get('review', {}).get('checklist', [])
        if review_checklist:
            lines.append("## Your Review Checklist:")
            for item in review_checklist:
                lines.append(f"  □ {item}")
            lines.append("")

        return "\n".join(lines)


def merge_context_with_persona(
    project_context: Dict[str, Any],
    persona_name: str,
    personas_dir: Path
) -> Dict[str, Any]:
    """
    Convenience function to merge project context with persona.

    Args:
        project_context: Project context dictionary
        persona_name: Name of persona to apply
        personas_dir: Directory containing persona files

    Returns:
        Combined context with persona applied
    """
    persona_mgr = PersonaManager(personas_dir)
    persona_config = persona_mgr.load_persona(persona_name)
    return persona_mgr.apply_persona_to_context(project_context, persona_config)
