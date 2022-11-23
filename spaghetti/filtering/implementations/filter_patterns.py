from typing import Dict, Set

from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.log import logger
from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies


class FilterPatternsFilter(ProjectDependenciesFilter):
    filtered_patterns: Set[str]
    show_unfiltered_dependencies: bool
    show_unfiltered_reverse_dependencies: bool

    def __init__(
        self,
        filtered_patterns: Set[str],
        *,
        show_unfiltered_dependencies: bool = True,
        show_unfiltered_reverse_dependencies: bool = True,
    ) -> None:
        self.filtered_patterns = filtered_patterns
        self.show_unfiltered_dependencies = show_unfiltered_dependencies
        self.show_unfiltered_reverse_dependencies = show_unfiltered_reverse_dependencies

    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        module_imports: Dict[Module, Set[Module]] = {}

        for module in self._get_filtered_modules(dependencies):
            new_links = set()

            if not self.show_unfiltered_reverse_dependencies and not self._is_module_filtered(
                module
            ):
                logger.debug("module_ignored", module=module)
                continue

            for link in dependencies.module_imports[module]:
                if not self._is_module_filtered(module) and not self._is_module_filtered(link):
                    # Ignore unfiltered links for unfiltered modules.
                    logger.debug("link_ignored", module=module, link=link)
                    continue

                if not self.show_unfiltered_dependencies and not self._is_module_filtered(link):
                    # Exclude unfiltered links
                    logger.debug("link_ignored", module=module, link=link)
                    continue

                if link != module:
                    new_links.add(link)

            if module not in module_imports:
                module_imports[module] = set()

            module_imports[module].update(new_links)

        return ProjectDependencies(module_imports=module_imports)

    def _get_filtered_modules(self, dependencies: ProjectDependencies) -> Set[Module]:
        filtered_modules = set()

        for module, links in dependencies.module_imports.items():
            skip_module = True

            for link in links:
                if self._is_module_filtered(link):
                    skip_module = False
                    break

            if skip_module and not self._is_module_filtered(module):
                logger.debug("module_ignored", module=module)
                continue

            filtered_modules.add(module)

        return filtered_modules

    def _is_module_filtered(self, module: Module) -> bool:
        if not self.filtered_patterns:
            return True

        return self._module_match_patterns(module, self.filtered_patterns)

    def _module_match_patterns(self, module: Module, patterns: Set[str]) -> bool:
        for pattern in patterns:
            if pattern in module.name:
                return True

        return False
