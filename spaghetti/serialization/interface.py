import abc

from spaghetti.models.project_dependencies import ProjectDependencies


class ProjectDependenciesSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, dependencies: ProjectDependencies) -> bytes:
        """Serialize dependencies."""

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> ProjectDependencies:
        """Deserialize dependencies from arbitrary data."""
