from typing import List

from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.models.project_dependencies import ProjectDependencies


class ProjectDependenciesFilterChain(ProjectDependenciesFilter):
    filters: List[ProjectDependenciesFilter]

    def __init__(self, filters: List[ProjectDependenciesFilter]):
        self.filters = filters

    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        for filt in self.filters:
            dependencies = filt.apply_filter(dependencies)
        return dependencies
