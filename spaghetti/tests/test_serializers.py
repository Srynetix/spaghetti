from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.implementations.json_serializer import (
    ProjectDependenciesJsonSerializer,
)


class TestJsonSerializer:
    def test_serialize(self, sample_dependencies: ProjectDependencies) -> None:
        serializer = ProjectDependenciesJsonSerializer()
        assert (
            serializer.serialize(sample_dependencies)
            == b'{"module.a": ["module.b", "sys"], "module.b": [], "module.c": ["module.b"]}'
        )

    def test_deserialize(self, sample_dependencies: ProjectDependencies) -> None:
        serializer = ProjectDependenciesJsonSerializer()
        assert (
            serializer.deserialize(
                b'{"module.a": ["module.b", "sys"], "module.b": [], "module.c": ["module.b"]}'
            )
            == sample_dependencies
        )
