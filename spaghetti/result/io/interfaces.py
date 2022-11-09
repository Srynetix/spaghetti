import abc

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultWriter(abc.ABC):
    @abc.abstractmethod
    def write(self, result: ParseResult, serializer: ParseResultSerializer) -> None:
        """Write the result through a serializer."""


class ParseResultReader(abc.ABC):
    @abc.abstractmethod
    def read(self, serializer: ParseResultSerializer) -> ParseResult:
        """Read the result through a serializer."""
