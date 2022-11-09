import abc

from spaghetti.models.parse_result import ParseResult


class ParseResultSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, result: ParseResult) -> bytes:
        """Serialize the result."""

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> ParseResult:
        """Deserialize the result from arbitrary data."""
