from typing import Dict, Set

from spaghetti.models.module import Module


class ParseResult:
    source_modules: Set[Module]
    import_links: Dict[Module, Set[Module]]

    def __init__(self, *, source_modules: Set[Module], import_links: Dict[Module, Set[Module]]) -> None:
        self.source_modules = source_modules
        self.import_links = import_links

    def get_module_dependency_count(self, module: Module) -> int:
        return len(self.import_links[module])

    def get_module_reverse_dependency_count(self, module: Module) -> int:
        count = 0
        for mod, links in self.import_links.items():
            if module in links:
                count += 1
        return count
