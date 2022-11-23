import abc

from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.interface import ProjectDependenciesSerializer


class ProjectDependenciesWriter(abc.ABC):
    @abc.abstractmethod
    def write(self, result: ProjectDependencies, serializer: ProjectDependenciesSerializer) -> None:
        """Write dependencies through a serializer."""


class ProjectDependenciesReader(abc.ABC):
    @abc.abstractmethod
    def read(self, serializer: ProjectDependenciesSerializer) -> ProjectDependencies:
        """Read dependencies through a serializer."""
