from typing import Dict, Set

from structlog import get_logger

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class FilterPatternsResultFilter(ParseResultFilter):
    filtered_patterns: Set[str]

    def __init__(
        self,
        filtered_patterns: Set[str],
    ) -> None:
        self.filtered_patterns = filtered_patterns
        self.logger = get_logger("FilterPatternsResultFilter")

    def apply_filter(self, result: ParseResult) -> ParseResult:
        module_imports: Dict[Module, Set[Module]] = {}

        for module in self._get_filtered_modules(result):
            new_links = set()
            for link in result.module_imports[module]:
                if not self._is_module_filtered(module) and not self._is_module_filtered(link):
                    # Ignore non-filtered links for non-filtered modules.
                    self.logger.debug("link_ignored", module=module, link=link)
                    continue

                if link != module:
                    new_links.add(link)

            if module not in module_imports:
                module_imports[module] = set()

            module_imports[module].update(new_links)

        return ParseResult(module_imports=module_imports)

    def _get_filtered_modules(self, result: ParseResult) -> Set[Module]:
        filtered_modules = set()

        for module, links in result.module_imports.items():
            skip_module = True

            for link in links:
                if self._is_module_filtered(link):
                    skip_module = False
                    break

            if skip_module and not self._is_module_filtered(module):
                self.logger.debug("module_ignored", module=module)
                continue

            filtered_modules.add(module)

        return filtered_modules

    def _is_module_filtered(self, module: Module) -> bool:
        if not self.filtered_patterns:
            return True

        return self._module_match_patterns(module, self.filtered_patterns)

    def _module_match_patterns(self, module: Module, patterns: Set[str]):
        for pattern in patterns:
            if module.name.startswith(pattern):
                return True

        return False
