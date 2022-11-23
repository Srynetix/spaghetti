from spaghetti.filtering.implementations.chain import ProjectDependenciesFilterChain
from spaghetti.filtering.implementations.filter_patterns import FilterPatternsFilter
from spaghetti.models.project_dependencies import ProjectDependencies


class TestFilterChain:
    def test_empty_chain(self, sample_dependencies: ProjectDependencies) -> None:
        filt = ProjectDependenciesFilterChain(filters=[])
        assert filt.apply_filter(sample_dependencies) == sample_dependencies

    def test_chain_with_no_effects(self, sample_dependencies: ProjectDependencies) -> None:
        filt = ProjectDependenciesFilterChain(
            filters=[FilterPatternsFilter(filtered_patterns=set())]
        )
        assert filt.apply_filter(sample_dependencies) == sample_dependencies
