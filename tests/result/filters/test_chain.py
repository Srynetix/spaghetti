from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.chain import ResultFilterChain
from spaghetti.result.filters.implementations.filter_patterns import (
    FilterPatternsResultFilter,
)


class TestResultFilterChain:
    def test_empty_chain(self, sample_parse_result: ParseResult) -> None:
        filt = ResultFilterChain(filters=[])
        assert filt.apply_filter(sample_parse_result) == sample_parse_result

    def test_chain_with_no_effects(self, sample_parse_result: ParseResult) -> None:
        filt = ResultFilterChain(filters=[FilterPatternsResultFilter(filtered_patterns=set())])
        assert filt.apply_filter(sample_parse_result) == sample_parse_result
