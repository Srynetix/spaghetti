from spaghetti.filtering.implementations.hide_modules_without_links import (
    HideModulesWithoutLinksFilter,
)
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestHideModulesWithoutLinksFilter:
    def test_filter(self, sample_dependencies: ProjectDependencies) -> None:
        filt = HideModulesWithoutLinksFilter()
        assert filt.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={
                Module("module.a"): {Module("sys"), Module("module.b")},
                Module("module.c"): {Module("module.b")},
            }
        )
