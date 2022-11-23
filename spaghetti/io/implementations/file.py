from pathlib import Path

from spaghetti.io.implementations.stream import (
    ProjectDependenciesStreamReader,
    ProjectDependenciesStreamWriter,
)
from spaghetti.io.interfaces import ProjectDependenciesReader, ProjectDependenciesWriter
from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.interface import ProjectDependenciesSerializer


class ProjectDependenciesFileWriter(ProjectDependenciesWriter):
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(
        self, dependencies: ProjectDependencies, serializer: ProjectDependenciesSerializer
    ) -> None:
        with open(self.path, mode="w", encoding="utf-8") as fd:
            writer = ProjectDependenciesStreamWriter(fd)
            writer.write(dependencies, serializer)


class ProjectDependenciesFileReader(ProjectDependenciesReader):
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self, serializer: ProjectDependenciesSerializer) -> ProjectDependencies:
        with open(self.path, mode="r", encoding="utf-8") as fd:
            reader = ProjectDependenciesStreamReader(fd)
            return reader.read(serializer)
