from typing import Dict, Set

from spaghetti.models.module import Module


class ProjectDependencies:
    module_imports: Dict[Module, Set[Module]]

    def __init__(self, *, module_imports: Dict[Module, Set[Module]]) -> None:
        self.module_imports = module_imports

    def get_module_dependency_count(self, module: Module) -> int:
        return len(self.module_imports[module])

    def get_module_reverse_dependency_count(self, module: Module) -> int:
        count = 0
        for _, links in self.module_imports.items():
            if module in links:
                count += 1
        return count

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.module_imports == other.module_imports

    def __str__(self) -> str:
        return str(self.module_imports)

    def __repr__(self) -> str:
        return str(self)
