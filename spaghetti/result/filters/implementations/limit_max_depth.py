from typing import Dict, Set

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class LimitMaxDepthResultFilter(ParseResultFilter):
    max_depth: int

    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth

    def _get_module_at_depth(self, module: Module) -> Module:
        if self.max_depth:
            return module.with_limited_depth(self.max_depth)
        return module

    def apply_filter(self, result: ParseResult) -> ParseResult:
        module_imports: Dict[Module, Set[Module]] = {}

        for module, links in result.module_imports.items():
            module_at_depth = self._get_module_at_depth(module)

            new_links = set()
            for link in links:
                link_at_depth = self._get_module_at_depth(link)
                if link_at_depth != module_at_depth:
                    new_links.add(link_at_depth)

            if module_at_depth not in module_imports:
                module_imports[module_at_depth] = set()
            module_imports[module_at_depth].update(new_links)

        return ParseResult(module_imports=module_imports)
