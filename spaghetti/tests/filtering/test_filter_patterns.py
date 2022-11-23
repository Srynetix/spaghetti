import pytest

from spaghetti.filtering.implementations.filter_patterns import FilterPatternsFilter
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestFilterPatternsFilter:
    @pytest.fixture
    def sample(self) -> ProjectDependencies:
        return ProjectDependencies(
            module_imports={
                Module("module.a"): {Module("module.b"), Module("sys")},
                Module("module.b"): {Module("typing")},
                Module("module.c"): {Module("module.b")},
                Module("module.d"): {Module("module.c")},
            },
        )

    def test_empty_filter(self, sample_dependencies: ProjectDependencies) -> None:
        filt = FilterPatternsFilter(filtered_patterns=set())
        assert filt.apply_filter(sample_dependencies) == sample_dependencies

    def test_filter(self, sample_dependencies: ProjectDependencies) -> None:
        conf_filter = FilterPatternsFilter(filtered_patterns={"module.a"})
        assert conf_filter.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={Module("module.a"): {Module("sys"), Module("module.b")}}
        )

    def test_filter_link(self, sample_dependencies: ProjectDependencies) -> None:
        conf_filter = FilterPatternsFilter(filtered_patterns={"module.b"})
        assert conf_filter.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={
                Module("module.c"): {Module("module.b")},
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
            }
        )

    def test_skip_unfiltered_dependencies(self, sample: ProjectDependencies) -> None:
        conf_filter = FilterPatternsFilter(
            filtered_patterns={"module.c"}, show_unfiltered_dependencies=False
        )
        assert conf_filter.apply_filter(sample) == ProjectDependencies(
            module_imports={Module("module.c"): set(), Module("module.d"): {Module("module.c")}}
        )

    def test_skip_unfiltered_reverse_dependencies(self, sample: ProjectDependencies) -> None:
        conf_filter = FilterPatternsFilter(
            filtered_patterns={"module.c"}, show_unfiltered_reverse_dependencies=False
        )
        assert conf_filter.apply_filter(sample) == ProjectDependencies(
            module_imports={Module("module.c"): {Module("module.b")}}
        )
