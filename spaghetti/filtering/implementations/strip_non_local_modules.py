from typing import Set

from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class StripNonLocalModulesFilter(ProjectDependenciesFilter):
    local_modules: Set[Module]

    def __init__(self, local_modules: Set[Module]) -> None:
        self.local_modules = local_modules

    def _get_filtered_links(self, links: Set[Module]) -> Set[Module]:
        return {link for link in links if link in self.local_modules}

    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        return ProjectDependencies(
            module_imports={
                module: self._get_filtered_links(links)
                for (module, links) in dependencies.module_imports.items()
            }
        )
