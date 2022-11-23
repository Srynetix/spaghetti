from typing import List, Optional, Set

from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.models.project_dependencies import ProjectDependencies

from .chain import ProjectDependenciesFilterChain
from .exclude_patterns import ExcludePatternsFilter
from .filter_patterns import FilterPatternsFilter
from .hide_modules_without_links import HideModulesWithoutLinksFilter
from .limit_max_depth import LimitMaxDepthFilter
from .strip_non_local_modules import StripNonLocalModulesFilter


class ConfigurableFilter(ProjectDependenciesFilter):
    excluded_patterns: Set[str]
    filtered_patterns: Set[str]
    show_unfiltered_dependencies: bool
    show_unfiltered_reverse_dependencies: bool
    max_depth: int
    hide_modules_without_links: bool
    strip_non_local_modules: bool

    def __init__(
        self,
        *,
        excluded_patterns: Optional[Set[str]] = None,
        filtered_patterns: Optional[Set[str]] = None,
        show_unfiltered_dependencies: bool = True,
        show_unfiltered_reverse_dependencies: bool = True,
        max_depth: int = 0,
        hide_modules_without_links: bool = True,
        strip_non_local_modules: bool = True,
    ) -> None:
        self.excluded_patterns = excluded_patterns or set()
        self.filtered_patterns = filtered_patterns or set()
        self.show_unfiltered_dependencies = show_unfiltered_dependencies
        self.show_unfiltered_reverse_dependencies = show_unfiltered_reverse_dependencies
        self.max_depth = max_depth
        self.hide_modules_without_links = hide_modules_without_links
        self.strip_non_local_modules = strip_non_local_modules

    def _build_filter_chain(
        self, dependencies: ProjectDependencies
    ) -> ProjectDependenciesFilterChain:
        local_modules = set(dependencies.module_imports.keys())
        filters: List[ProjectDependenciesFilter] = []

        if self.max_depth > 0:
            filters.append(LimitMaxDepthFilter(self.max_depth))
        if self.excluded_patterns:
            filters.append(ExcludePatternsFilter(self.excluded_patterns))
        if self.filtered_patterns:
            filters.append(
                FilterPatternsFilter(
                    self.filtered_patterns,
                    show_unfiltered_dependencies=self.show_unfiltered_dependencies,
                    show_unfiltered_reverse_dependencies=self.show_unfiltered_reverse_dependencies,
                )
            )
        if self.strip_non_local_modules:
            filters.append(StripNonLocalModulesFilter(local_modules))
        if self.hide_modules_without_links:
            filters.append(HideModulesWithoutLinksFilter())

        return ProjectDependenciesFilterChain(filters)

    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        chain = self._build_filter_chain(dependencies)
        return chain.apply_filter(dependencies)
