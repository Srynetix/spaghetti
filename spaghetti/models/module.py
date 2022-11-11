import functools
from pathlib import Path
from typing import List, Optional


@functools.total_ordering
class Module:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_path(cls, root: Path, path: Path) -> "Module":
        local_path = path.relative_to(root)
        name = ".".join(local_path.parts).replace(".__init__.py", "").replace(".py", "")
        return cls(name=name)

    def join(self, name: str) -> "Module":
        return type(self)(name=self.name + "." + name)

    def parent(self) -> Optional["Module"]:
        parts = self.parts()
        if len(parts) > 1:
            return type(self)(name=".".join(parts[:-1]))
        return None

    def parts(self) -> List[str]:
        return self.name.split(".")

    def with_limited_depth(self, depth: int) -> "Module":
        parts = self.parts()
        new_parts = parts[:depth]
        return type(self)(name=".".join(new_parts))

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.name == other.name

    def __lt__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.name < other.name

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self)
