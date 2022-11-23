from spaghetti.filtering.implementations.strip_non_local_modules import (
    StripNonLocalModulesFilter,
)
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestStripNonLocalModulesFilter:
    def test_filter(self, sample_dependencies: ProjectDependencies) -> None:
        filt = StripNonLocalModulesFilter(
            local_modules={Module("module.a"), Module("module.b"), Module("module.c")}
        )
        assert filt.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
                Module("module.c"): {Module("module.b")},
            }
        )
