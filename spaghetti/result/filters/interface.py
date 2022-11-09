import abc

from spaghetti.models.parse_result import ParseResult


class ParseResultFilter(abc.ABC):
    @abc.abstractmethod
    def apply_filter(self, result: ParseResult) -> ParseResult:
        """Transform the result into another result."""
