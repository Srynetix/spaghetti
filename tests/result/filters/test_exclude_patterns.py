from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.exclude_patterns import (
    ExcludePatternsResultFilter,
)


class TestExcludePatternsResultFilter:
    def test_empty_filter(self, sample_parse_result: ParseResult):
        filt = ExcludePatternsResultFilter(excluded_patterns=set())
        assert filt.apply_filter(sample_parse_result) == sample_parse_result

    def test_exclude_module(self, sample_parse_result: ParseResult):
        filt = ExcludePatternsResultFilter(excluded_patterns={"module.a"})
        assert filt.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.b"): set(), Module("module.c"): {Module("module.b")}}
        )

    def test_exclude_link(self, sample_parse_result: ParseResult):
        filt = ExcludePatternsResultFilter(excluded_patterns={"module.b"})
        assert filt.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.a"): {Module("sys")}, Module("module.c"): set()}
        )
