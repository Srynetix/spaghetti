from typing import Dict, Set

from structlog import get_logger

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class ExcludePatternsResultFilter(ParseResultFilter):
    excluded_patterns: Set[str]

    def __init__(self, excluded_patterns: Set[str]) -> None:
        self.excluded_patterns = excluded_patterns
        self.logger = get_logger("ExcludePatternsResultFilter")

    def apply_filter(self, result: ParseResult) -> ParseResult:
        module_imports: Dict[Module, Set[Module]] = {}

        for module in result.module_imports:
            if self._is_module_excluded(module):
                self.logger.debug("module_excluded", module=module)
                continue

            new_links = set()
            for link in result.module_imports[module]:
                if self._is_module_excluded(link):
                    self.logger.debug("link_excluded", module=module, link=link)
                    continue

                if link != module:
                    new_links.add(link)

            if module not in module_imports:
                module_imports[module] = set()
            module_imports[module].update(new_links)

        return ParseResult(module_imports=module_imports)

    def _is_module_excluded(self, module: Module) -> bool:
        return self._module_match_patterns(module, self.excluded_patterns)

    def _module_match_patterns(self, module: Module, patterns: Set[str]) -> bool:
        for pattern in patterns:
            if module.name.startswith(pattern):
                return True
        return False
