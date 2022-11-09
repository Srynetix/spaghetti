import abc

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultWriter(abc.ABC):
    @abc.abstractmethod
    def write(self, result: ParseResult, serializer: ParseResultSerializer) -> None:
        pass


class ParseResultReader(abc.ABC):
    @abc.abstractmethod
    def read(self, serializer: ParseResultSerializer) -> ParseResult:
        pass
