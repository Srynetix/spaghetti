import abc

from spaghetti.models.project_dependencies import ProjectDependencies


class ProjectDependenciesFilter(abc.ABC):
    @abc.abstractmethod
    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        """Transform the project dependencies."""
