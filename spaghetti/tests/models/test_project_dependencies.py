import pytest

from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestProjectDependencies:
    @pytest.fixture
    def arrange(self) -> ProjectDependencies:
        return ProjectDependencies(
            module_imports={
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
                Module("module.c"): {Module("module.b")},
            },
        )

    def test_get_module_dependency_count(self, arrange: ProjectDependencies) -> None:
        assert arrange.get_module_dependency_count(Module("module.a")) == 1
        assert arrange.get_module_dependency_count(Module("module.b")) == 0
        assert arrange.get_module_dependency_count(Module("module.c")) == 1

    def test_get_module_reverse_dependency_count(self, arrange: ProjectDependencies) -> None:
        assert arrange.get_module_reverse_dependency_count(Module("module.a")) == 0
        assert arrange.get_module_reverse_dependency_count(Module("module.b")) == 2
        assert arrange.get_module_reverse_dependency_count(Module("module.c")) == 0

    def test_str(self, arrange: ProjectDependencies) -> None:
        assert str(arrange) != ""

    def test_repr(self, arrange: ProjectDependencies) -> None:
        assert repr(arrange) != ""
