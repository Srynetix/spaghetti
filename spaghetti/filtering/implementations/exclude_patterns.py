from typing import Dict, Set

from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.log import logger
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class ExcludePatternsFilter(ProjectDependenciesFilter):
    excluded_patterns: Set[str]

    def __init__(self, excluded_patterns: Set[str]) -> None:
        self.excluded_patterns = excluded_patterns

    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        module_imports: Dict[Module, Set[Module]] = {}

        for module in dependencies.module_imports:
            if self._is_module_excluded(module):
                logger.debug("module_excluded", module=module)
                continue

            new_links = set()
            for link in dependencies.module_imports[module]:
                if self._is_module_excluded(link):
                    logger.debug("link_excluded", module=module, link=link)
                    continue

                if link != module:
                    new_links.add(link)

            if module not in module_imports:
                module_imports[module] = set()
            module_imports[module].update(new_links)

        return ProjectDependencies(module_imports=module_imports)

    def _is_module_excluded(self, module: Module) -> bool:
        return self._module_match_patterns(module, self.excluded_patterns)

    def _module_match_patterns(self, module: Module, patterns: Set[str]) -> bool:
        for pattern in patterns:
            if pattern in module.name:
                return True
        return False
