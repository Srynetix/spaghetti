from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.strip_non_local_modules import (
    StripNonLocalModulesResultFilter,
)


class TestStripNonLocalModulesResultFilter:
    def test_filter(self, sample_parse_result: ParseResult):
        filt = StripNonLocalModulesResultFilter(
            local_modules={Module("module.a"), Module("module.b"), Module("module.c")}
        )
        assert filt.apply_filter(sample_parse_result) == ParseResult(
            module_imports={
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
                Module("module.c"): {Module("module.b")},
            }
        )
