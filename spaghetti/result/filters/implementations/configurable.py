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
        excluded_patterns: Optional[List],
        filtered_patterns: Optional[List],
    ) -> None:
        self.strip_non_local_modules = strip_non_local_modules
        self.hide_modules_without_links = hide_modules_without_links
        self.max_depth = max_depth
        self.excluded_patterns = excluded_patterns or []
        self.filtered_patterns = filtered_patterns or []

    def _get_module_at_depth(self, module: Module) -> Module:
        if self.max_depth:
            return module.with_limited_depth(self.max_depth)
        return module

    def _is_module_excluded(self, module: Module) -> bool:
        for pattern in self.excluded_patterns:
            if module.name.startswith(pattern):
                return True
        return False

    def _get_filtered_modules(self, modules: Set[Module]) -> Set[Module]:
        filtered_modules = set()
        for module in modules:
            if self.filtered_patterns:
                skip_module = True
                for pattern in self.filtered_patterns:
                    if module.name.startswith(pattern):
                        skip_module = False
                        break
                if skip_module:
                    continue
            filtered_modules.add(module)
        return filtered_modules

    def apply_filter(self, result: ParseResult) -> ParseResult:
        source_modules = set()
        import_links: Dict[Module, Set[Module]] = {}

        for module in self._get_filtered_modules(result.source_modules):
            module_at_depth = self._get_module_at_depth(module)
            if self._is_module_excluded(module_at_depth):
                continue

            links = result.import_links[module]
            new_links = set()
            for link in links:
                if self.strip_non_local_modules and link not in result.source_modules:
                    continue

                link_at_depth = self._get_module_at_depth(link)
                if self._is_module_excluded(link_at_depth):
                    continue

                if link_at_depth != module_at_depth:
                    new_links.add(link_at_depth)

            if self.hide_modules_without_links and len(new_links) == 0:
                continue

            source_modules.add(module_at_depth)
            if module not in import_links:
                import_links[module_at_depth] = set()
            import_links[module_at_depth].update(new_links)

        return ParseResult(source_modules=source_modules, import_links=import_links)
