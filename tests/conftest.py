import pytest

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult


@pytest.fixture
def sample_parse_result() -> ParseResult:
    return ParseResult(
        module_imports={
            Module("module.a"): {Module("module.b"), Module("sys")},
            Module("module.b"): set(),
            Module("module.c"): {Module("module.b")},
        },
    )
