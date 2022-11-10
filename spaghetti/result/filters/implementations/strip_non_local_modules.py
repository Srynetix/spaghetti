from typing import Set

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class StripNonLocalModulesResultFilter(ParseResultFilter):
    local_modules: Set[Module]

    def __init__(self, local_modules: Set[Module]) -> None:
        self.local_modules = local_modules

    def _get_filtered_links(self, links: Set[Module]) -> Set[Module]:
        return {link for link in links if link in self.local_modules}

    def apply_filter(self, result: ParseResult) -> ParseResult:
        return ParseResult(
            module_imports={
                module: self._get_filtered_links(links)
                for (module, links) in result.module_imports.items()
            }
        )
