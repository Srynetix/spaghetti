from abc import ABC, abstractmethod

from spaghetti.models.project_dependencies import ProjectDependencies


class Report(ABC):
    @abstractmethod
    def render(self, dependencies: ProjectDependencies) -> None:
        """Render the report."""
