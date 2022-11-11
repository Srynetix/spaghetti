from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.filter_patterns import (
    FilterPatternsResultFilter,
)


class TestFilterPatternsResultFilter:
    def test_empty_filter(self, sample_parse_result: ParseResult) -> None:
        filt = FilterPatternsResultFilter(filtered_patterns=set())
        assert filt.apply_filter(sample_parse_result) == sample_parse_result

    def test_filter(self, sample_parse_result: ParseResult) -> None:
        conf_filter = FilterPatternsResultFilter(filtered_patterns={"module.a"})
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.a"): {Module("sys"), Module("module.b")}}
        )

    def test_filter_link(self, sample_parse_result: ParseResult) -> None:
        conf_filter = FilterPatternsResultFilter(filtered_patterns={"module.b"})
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={
                Module("module.c"): {Module("module.b")},
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
            }
        )
