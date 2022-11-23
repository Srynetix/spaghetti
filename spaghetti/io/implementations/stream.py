from typing import IO, Any

from spaghetti.io.interfaces import ProjectDependenciesReader, ProjectDependenciesWriter
from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.interface import ProjectDependenciesSerializer


class ProjectDependenciesStreamWriter(ProjectDependenciesWriter):
    stream: IO[Any]

    def __init__(self, stream: IO[Any]) -> None:
        self.stream = stream

    def write(
        self, dependencies: ProjectDependencies, serializer: ProjectDependenciesSerializer
    ) -> None:
        self.stream.write(serializer.serialize(dependencies).decode("utf-8"))


class ProjectDependenciesStreamReader(ProjectDependenciesReader):
    stream: IO[Any]

    def __init__(self, stream: IO[Any]) -> None:
        self.stream = stream

    def read(self, serializer: ProjectDependenciesSerializer) -> ProjectDependencies:
        return serializer.deserialize(self.stream.read())
