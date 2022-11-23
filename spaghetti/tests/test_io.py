from pathlib import Path
from typing import Any

from spaghetti.io.implementations.file import (
    ProjectDependenciesFileReader,
    ProjectDependenciesFileWriter,
)
from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.interface import ProjectDependenciesSerializer


class DummySerializer(ProjectDependenciesSerializer):
    source: ProjectDependencies

    def __init__(self, source: ProjectDependencies) -> None:
        self.source = source

    def serialize(self, dependencies: ProjectDependencies) -> bytes:
        return b"serialized"

    def deserialize(self, data: bytes) -> ProjectDependencies:
        return self.source


class TestFileIO:
    def test_write(self, sample_dependencies: ProjectDependencies, tmpdir: Any) -> None:
        target_file = Path(tmpdir.join("file.dat"))
        serializer = DummySerializer(sample_dependencies)

        writer = ProjectDependenciesFileWriter(target_file)
        writer.write(sample_dependencies, serializer)
        assert target_file.read_bytes() == b"serialized"

    def test_read(self, sample_dependencies: ProjectDependencies, tmpdir: Any) -> None:
        target_file = Path(tmpdir.join("file.dat"))
        target_file.write_bytes(b"serialize")
        serializer = DummySerializer(sample_dependencies)

        reader = ProjectDependenciesFileReader(target_file)
        assert reader.read(serializer) == sample_dependencies
