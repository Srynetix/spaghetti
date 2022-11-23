import pytest

from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


@pytest.fixture
def sample_dependencies() -> ProjectDependencies:
    return ProjectDependencies(
        module_imports={
            Module("module.a"): {Module("module.b"), Module("sys")},
            Module("module.b"): set(),
            Module("module.c"): {Module("module.b")},
        },
    )
