from pathlib import Path

import pytest

from spaghetti.models.module import Module


class TestModule:
    @pytest.mark.parametrize(
        "root,path,module",
        (
            ("./", "./module/and/then.py", "module.and.then"),
            ("./", "./module/and/then/__init__.py", "module.and.then"),
            ("./root", "./root/module/and/then/__init__.py", "module.and.then"),
        ),
    )
    def test_from_path(self, root: str, path: str, module: str) -> None:
        assert Module.from_path(Path(root), Path(path)) == Module(module)

    def test_join(self) -> None:
        assert Module("module").join("and") == Module("module.and")
        assert Module("module.and").join("then") == Module("module.and.then")

    def test_parent(self) -> None:
        def parent(module: Module) -> Module:
            parent = module.parent()
            assert parent is not None
            return parent

        module = Module("module.and.then")
        assert parent(module) == Module("module.and")
        assert parent(parent(module)) == Module("module")
        assert parent(parent(module)).parent() is None

    def test_parts(self) -> None:
        assert Module("module.and.then").parts() == ["module", "and", "then"]

    def test_with_limited_depth(self) -> None:
        assert Module("module.and.then").with_limited_depth(1) == Module("module")
        assert Module("module.and.then").with_limited_depth(2) == Module("module.and")
        assert Module("module.and.then").with_limited_depth(3) == Module("module.and.then")
        assert Module("module.and.then").with_limited_depth(4) == Module("module.and.then")

    def test_equality(self) -> None:
        assert Module("module") == Module("module")

    def test_ord(self) -> None:
        assert Module("module.a") < Module("module.b")

    def test_hash(self) -> None:
        assert {Module("module.a"), Module("module.b")}
