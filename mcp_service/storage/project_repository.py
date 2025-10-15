"""Git-backed project repository storage system."""
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from ai_sdlc_config import ConfigManager


@dataclass
class ProjectMetadata:
    """Metadata for a project."""
    name: str
    project_type: str  # base, methodology, custom, merged
    version: str
    created: str
    modified: str
    base_projects: List[str]  # Projects this inherits from
    description: Optional[str] = None
    merged_from: Optional[List[str]] = None  # For merged projects
    merge_date: Optional[str] = None  # For merged projects
    runtime_overrides: Optional[Dict[str, Any]] = None  # For merged projects


class ProjectRepository:
    """
    Manages projects in a git-backed repository.

    Repository structure:
        projects_repo/
        ├── .git/
        ├── projects.json              # Project registry
        ├── project_name_1/
        │   ├── project.json          # Project metadata
        │   ├── config/
        │   │   └── config.yml        # Configuration
        │   └── docs/                 # Referenced documents
        │       └── *.md
        └── merged_projects/
            └── merged_name/
                ├── project.json
                ├── config/
                │   └── merged.yml
                └── .merge_info.json  # Merge provenance
    """

    def __init__(self, repo_path: Path):
        """
        Initialize project repository.

        Args:
            repo_path: Path to repository root
        """
        self.repo_path = Path(repo_path).resolve()
        self.projects_file = self.repo_path / "projects.json"
        self.merged_projects_dir = self.repo_path / "merged_projects"

        # Initialize if not a git repository
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            self._initialize_repository()

    def _initialize_repository(self):
        """Initialize a new repository."""
        self.repo_path.mkdir(parents=True, exist_ok=True)
        self.merged_projects_dir.mkdir(exist_ok=True)

        # Initialize git
        try:
            result = subprocess.run(
                ["git", "init"],
                cwd=str(self.repo_path),
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git init failed: {e.stderr}") from e

        # Verify .git directory was created
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise RuntimeError(f"Git init failed - no .git directory at {git_dir}")

        # Configure git user (required for commits)
        subprocess.run(
            ["git", "config", "user.name", "AI_SDLC_Context"],
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["git", "config", "user.email", "ai-sdlc-config@localhost"],
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True
        )

        # Create projects registry
        self._save_projects_registry({})

        # Initial commit
        self._git_add_commit("Initialize project repository")

    def _load_projects_registry(self) -> Dict[str, Dict[str, Any]]:
        """Load projects registry."""
        if not self.projects_file.exists():
            return {}

        with open(self.projects_file, 'r') as f:
            return json.load(f)

    def _save_projects_registry(self, registry: Dict[str, Dict[str, Any]]):
        """Save projects registry."""
        with open(self.projects_file, 'w') as f:
            json.dump(registry, f, indent=2)

    def _git_add_commit(self, message: str):
        """Add all changes and commit."""
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=str(self.repo_path),
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git add failed: {e.stderr}") from e

        try:
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=str(self.repo_path),
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git commit failed: {e.stderr}") from e

    def create_project(
        self,
        name: str,
        project_type: str,
        base_projects: List[str],
        config: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> ProjectMetadata:
        """
        Create a new project.

        Args:
            name: Project name (must be unique)
            project_type: base, methodology, custom
            base_projects: List of base project names to inherit from
            config: Initial configuration (optional)
            description: Project description

        Returns:
            ProjectMetadata for created project

        Raises:
            ValueError: If project already exists
        """
        # Validate
        registry = self._load_projects_registry()
        if name in registry:
            raise ValueError(f"Project '{name}' already exists")

        # Create project directory
        project_dir = self.repo_path / name
        project_dir.mkdir(parents=True)

        config_dir = project_dir / "config"
        config_dir.mkdir()

        docs_dir = project_dir / "docs"
        docs_dir.mkdir()

        # Create metadata
        now = datetime.utcnow().isoformat() + "Z"
        metadata = ProjectMetadata(
            name=name,
            project_type=project_type,
            version="1.0.0",
            created=now,
            modified=now,
            base_projects=base_projects,
            description=description
        )

        # Save metadata
        metadata_file = project_dir / "project.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

        # Save config if provided
        if config:
            from ai_sdlc_config.loaders.yaml_loader import YAMLLoader
            import yaml

            config_file = config_dir / "config.yml"
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        else:
            # Create empty structure
            config_file = config_dir / "config.yml"
            config_file.write_text("# Configuration for {}\n".format(name))

        # Update registry
        registry[name] = {
            "type": project_type,
            "path": str(project_dir.relative_to(self.repo_path)),
            "base_projects": base_projects
        }
        self._save_projects_registry(registry)

        # Commit
        self._git_add_commit(f"Create project: {name}")

        return metadata

    def get_project(self, name: str) -> Optional[ProjectMetadata]:
        """
        Get project metadata.

        Args:
            name: Project name

        Returns:
            ProjectMetadata or None if not found
        """
        registry = self._load_projects_registry()
        if name not in registry:
            return None

        project_dir = self.repo_path / registry[name]["path"]
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            return None

        with open(metadata_file, 'r') as f:
            data = json.load(f)
            return ProjectMetadata(**data)

    def list_projects(self) -> List[ProjectMetadata]:
        """
        List all projects.

        Returns:
            List of ProjectMetadata
        """
        registry = self._load_projects_registry()
        projects = []

        for name in registry:
            metadata = self.get_project(name)
            if metadata:
                projects.append(metadata)

        return projects

    def update_project(
        self,
        name: str,
        updates: Dict[str, Any]
    ) -> ProjectMetadata:
        """
        Update project configuration.

        Args:
            name: Project name
            updates: Dict of dot-path to value updates
                    e.g., {"methodology.testing.min_coverage": 95}

        Returns:
            Updated ProjectMetadata

        Raises:
            ValueError: If project doesn't exist
        """
        metadata = self.get_project(name)
        if not metadata:
            raise ValueError(f"Project '{name}' not found")

        registry = self._load_projects_registry()
        project_dir = self.repo_path / registry[name]["path"]
        config_file = project_dir / "config" / "config.yml"

        # Load current config
        from ai_sdlc_config.loaders.yaml_loader import YAMLLoader
        import yaml

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f) or {}

        # Apply updates
        for path, value in updates.items():
            parts = path.split('.')
            current = config

            # Navigate to parent
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Set value
            current[parts[-1]] = value

        # Save updated config
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        # Update metadata modified time
        metadata.modified = datetime.utcnow().isoformat() + "Z"
        metadata_file = project_dir / "project.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

        # Commit
        self._git_add_commit(f"Update project: {name}")

        return metadata

    def delete_project(self, name: str):
        """
        Delete a project.

        Args:
            name: Project name

        Raises:
            ValueError: If project doesn't exist
        """
        metadata = self.get_project(name)
        if not metadata:
            raise ValueError(f"Project '{name}' not found")

        registry = self._load_projects_registry()
        project_dir = self.repo_path / registry[name]["path"]

        # Remove directory
        shutil.rmtree(project_dir)

        # Update registry
        del registry[name]
        self._save_projects_registry(registry)

        # Commit
        self._git_add_commit(f"Delete project: {name}")

    def add_document(
        self,
        project_name: str,
        doc_path: str,
        content: str
    ) -> Path:
        """
        Add a document to a project.

        Args:
            project_name: Project name
            doc_path: Relative path within docs/ (e.g., "policies/security.md")
            content: Document content

        Returns:
            Absolute path to created document

        Raises:
            ValueError: If project doesn't exist
        """
        metadata = self.get_project(project_name)
        if not metadata:
            raise ValueError(f"Project '{project_name}' not found")

        registry = self._load_projects_registry()
        project_dir = self.repo_path / registry[project_name]["path"]
        docs_dir = project_dir / "docs"

        # Create document
        doc_file = docs_dir / doc_path
        doc_file.parent.mkdir(parents=True, exist_ok=True)
        doc_file.write_text(content)

        # Commit
        self._git_add_commit(f"Add document to {project_name}: {doc_path}")

        return doc_file

    def merge_projects(
        self,
        source_projects: List[str],
        target_name: str,
        runtime_overrides: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> ProjectMetadata:
        """
        Merge multiple projects into a new merged project.

        Args:
            source_projects: List of project names to merge (priority order)
            target_name: Name for merged project
            runtime_overrides: Additional runtime overrides to apply
            description: Description for merged project

        Returns:
            ProjectMetadata for merged project

        Raises:
            ValueError: If any source project doesn't exist or target exists
        """
        # Validate source projects exist
        for name in source_projects:
            if not self.get_project(name):
                raise ValueError(f"Source project '{name}' not found")

        # Check target doesn't exist
        registry = self._load_projects_registry()
        if target_name in registry:
            raise ValueError(f"Target project '{target_name}' already exists")

        # Create merged project directory
        merged_dir = self.merged_projects_dir / target_name
        merged_dir.mkdir(parents=True)

        config_dir = merged_dir / "config"
        config_dir.mkdir()

        # Perform merge using ConfigManager
        manager = ConfigManager(base_path=self.repo_path)

        for project_name in source_projects:
            project_dir = self.repo_path / registry[project_name]["path"]
            config_file = project_dir / "config" / "config.yml"

            if config_file.exists():
                # Load relative to repo root
                rel_path = config_file.relative_to(self.repo_path)
                manager.load_hierarchy(str(rel_path))

        # Apply runtime overrides
        if runtime_overrides:
            manager.add_runtime_overrides(runtime_overrides)

        # Merge
        manager.merge()

        # Export merged config
        import yaml
        merged_config_file = config_dir / "merged.yml"

        # Convert merged hierarchy to dict
        def hierarchy_to_dict(node) -> Dict[str, Any]:
            result = {}

            if node.value is not None and not node.children:
                # Leaf node
                from ai_sdlc_config.models.hierarchy_node import URIReference
                if isinstance(node.value, URIReference):
                    return {"uri": node.value.uri}
                else:
                    return node.value

            # Branch node
            for key, child in node.children.items():
                result[key] = hierarchy_to_dict(child)

            return result

        merged_dict = hierarchy_to_dict(manager.merged_hierarchy)

        with open(merged_config_file, 'w') as f:
            yaml.dump(merged_dict, f, default_flow_style=False, sort_keys=False)

        # Create merge info
        merge_info = {
            "source_projects": source_projects,
            "merge_date": datetime.utcnow().isoformat() + "Z",
            "runtime_overrides": runtime_overrides
        }

        merge_info_file = merged_dir / ".merge_info.json"
        with open(merge_info_file, 'w') as f:
            json.dump(merge_info, f, indent=2)

        # Create metadata
        now = datetime.utcnow().isoformat() + "Z"
        metadata = ProjectMetadata(
            name=target_name,
            project_type="merged",
            version="1.0.0",
            created=now,
            modified=now,
            base_projects=source_projects,
            description=description or f"Merged from: {', '.join(source_projects)}",
            merged_from=source_projects,
            merge_date=now,
            runtime_overrides=runtime_overrides
        )

        # Save metadata
        metadata_file = merged_dir / "project.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

        # Update registry
        registry[target_name] = {
            "type": "merged",
            "path": str(merged_dir.relative_to(self.repo_path)),
            "base_projects": source_projects,
            "merged_from": source_projects
        }
        self._save_projects_registry(registry)

        # Commit
        self._git_add_commit(f"Merge projects into {target_name}: {', '.join(source_projects)}")

        return metadata

    def get_project_config(self, name: str) -> Optional[ConfigManager]:
        """
        Get ConfigManager for a project with all its base projects loaded.

        Args:
            name: Project name

        Returns:
            ConfigManager with project hierarchy or None if not found
        """
        metadata = self.get_project(name)
        if not metadata:
            return None

        registry = self._load_projects_registry()
        manager = ConfigManager(base_path=self.repo_path)

        # Load base projects first (if not merged)
        if metadata.project_type != "merged":
            for base_name in metadata.base_projects:
                if base_name in registry:
                    base_dir = self.repo_path / registry[base_name]["path"]
                    base_config = base_dir / "config" / "config.yml"

                    if base_config.exists():
                        rel_path = base_config.relative_to(self.repo_path)
                        manager.load_hierarchy(str(rel_path))

        # Load project config
        project_dir = self.repo_path / registry[name]["path"]

        if metadata.project_type == "merged":
            config_file = project_dir / "config" / "merged.yml"
        else:
            config_file = project_dir / "config" / "config.yml"

        if config_file.exists():
            rel_path = config_file.relative_to(self.repo_path)
            manager.load_hierarchy(str(rel_path))

        # Merge
        manager.merge()

        return manager
