from spaghetti.filtering.implementations.exclude_patterns import ExcludePatternsFilter
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestExcludePatternsFilter:
    def test_empty_filter(self, sample_dependencies: ProjectDependencies) -> None:
        filt = ExcludePatternsFilter(excluded_patterns=set())
        assert filt.apply_filter(sample_dependencies) == sample_dependencies

    def test_exclude_module(self, sample_dependencies: ProjectDependencies) -> None:
        filt = ExcludePatternsFilter(excluded_patterns={"module.a"})
        assert filt.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={Module("module.b"): set(), Module("module.c"): {Module("module.b")}}
        )

    def test_exclude_link(self, sample_dependencies: ProjectDependencies) -> None:
        filt = ExcludePatternsFilter(excluded_patterns={"module.b"})
        assert filt.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={Module("module.a"): {Module("sys")}, Module("module.c"): set()}
        )
