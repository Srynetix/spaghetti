from typing import List

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class ResultFilterChain(ParseResultFilter):
    filters: List[ParseResultFilter]

    def __init__(self, filters: List[ParseResultFilter]):
        self.filters = filters

    def apply_filter(self, result: ParseResult) -> ParseResult:
        for filt in self.filters:
            result = filt.apply_filter(result)
        return result
