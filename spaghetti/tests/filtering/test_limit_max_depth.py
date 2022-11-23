from spaghetti.filtering.implementations.limit_max_depth import LimitMaxDepthFilter
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class TestLimitMaxDepthFilter:
    def test_filter_zero(self, sample_dependencies: ProjectDependencies) -> None:
        filt = LimitMaxDepthFilter(max_depth=0)
        assert filt.apply_filter(sample_dependencies) == sample_dependencies

    def test_filter(self, sample_dependencies: ProjectDependencies) -> None:
        filt = LimitMaxDepthFilter(max_depth=1)
        assert filt.apply_filter(sample_dependencies) == ProjectDependencies(
            module_imports={Module("module"): {Module("sys")}}
        )
