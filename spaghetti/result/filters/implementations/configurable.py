from typing import Dict, List, Optional, Set

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class ConfigurableResultFilter(ParseResultFilter):
    strip_non_local_modules: bool
    hide_modules_without_links: bool
    max_depth: Optional[int]
    excluded_patterns: List[str]
    filtered_patterns: List[str]

    def __init__(
        self,
        *,
        strip_non_local_modules: bool = False,
        hide_modules_without_links: bool = False,
        max_depth: Optional[int] = None,
        excluded_patterns: Optional[List] = None,
        filtered_patterns: Optional[List] = None,
    ) -> None:
        self.strip_non_local_modules = strip_non_local_modules
        self.hide_modules_without_links = hide_modules_without_links
        self.max_depth = max_depth
        self.excluded_patterns = excluded_patterns or []
        self.filtered_patterns = filtered_patterns or []

    def apply_filter(self, result: ParseResult) -> ParseResult:
        module_imports: Dict[Module, Set[Module]] = {}

        for module in sorted(self._get_filtered_modules(set(result.module_imports.keys()))):
            module_at_depth = self._get_module_at_depth(module)
            if self._is_module_excluded(module_at_depth):
                continue

            new_links = set()
            for link in sorted(result.module_imports[module]):
                if self.strip_non_local_modules and link not in result.module_imports:
                    continue

                link_at_depth = self._get_module_at_depth(link)
                if self._is_module_excluded(link_at_depth):
                    continue

                if link_at_depth != module_at_depth:
                    new_links.add(link_at_depth)

            if self.hide_modules_without_links and len(new_links) == 0:
                continue

            if module_at_depth not in module_imports:
                module_imports[module_at_depth] = set()
            module_imports[module_at_depth].update(new_links)

        return ParseResult(module_imports=module_imports)

    def _get_filtered_modules(self, modules: Set[Module]) -> Set[Module]:
        return {module for module in modules if self._is_module_filtered(module)}

    def _get_module_at_depth(self, module: Module) -> Module:
        if self.max_depth:
            return module.with_limited_depth(self.max_depth)
        return module

    def _is_module_excluded(self, module: Module) -> bool:
        return self._module_match_patterns(module, self.excluded_patterns)

    def _is_module_filtered(self, module: Module) -> bool:
        if not self.filtered_patterns:
            return True
        return self._module_match_patterns(module, self.filtered_patterns)

    def _module_match_patterns(self, module: Module, patterns: List[str]):
        for pattern in patterns:
            if module.name.startswith(pattern):
                return True
        return False
