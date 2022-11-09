import pytest

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult


class TestParseResult:
    @pytest.fixture
    def arrange(self) -> ParseResult:
        return ParseResult(
            module_imports={
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
                Module("module.c"): {Module("module.b")},
            },
        )

    def test_get_module_dependency_count(self, arrange: ParseResult):
        assert arrange.get_module_dependency_count(Module("module.a")) == 1
        assert arrange.get_module_dependency_count(Module("module.b")) == 0
        assert arrange.get_module_dependency_count(Module("module.c")) == 1

    def test_get_module_reverse_dependency_count(self, arrange: ParseResult):
        assert arrange.get_module_reverse_dependency_count(Module("module.a")) == 0
        assert arrange.get_module_reverse_dependency_count(Module("module.b")) == 2
        assert arrange.get_module_reverse_dependency_count(Module("module.c")) == 0
