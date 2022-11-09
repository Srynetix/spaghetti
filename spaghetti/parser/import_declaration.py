from typing import FrozenSet, Optional


class ImportDeclaration:
    source: Optional[str]
    modules: FrozenSet[str]

    def __init__(self, *, source: Optional[str], modules: Optional[FrozenSet[str]]) -> None:
        self.source = source
        self.modules = modules or frozenset()

    def __hash__(self) -> int:
        return hash((self.source, self.modules))

    def __str__(self) -> str:
        if self.source:
            return f"from {self.source} import {set(self.modules)}"
        return f"import {set(self.modules)}"

    def __repr__(self) -> str:
        return str(self)
