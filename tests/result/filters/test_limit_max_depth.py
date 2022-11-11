from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.limit_max_depth import (
    LimitMaxDepthResultFilter,
)


class TestLimitMaxDepthResultFilter:
    def test_filter_zero(self, sample_parse_result: ParseResult) -> None:
        filt = LimitMaxDepthResultFilter(max_depth=0)
        assert filt.apply_filter(sample_parse_result) == sample_parse_result

    def test_filter(self, sample_parse_result: ParseResult) -> None:
        filt = LimitMaxDepthResultFilter(max_depth=1)
        assert filt.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module"): {Module("sys")}}
        )
