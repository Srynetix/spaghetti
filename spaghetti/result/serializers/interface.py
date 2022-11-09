import abc

from spaghetti.models.parse_result import ParseResult


class ParseResultSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, result: ParseResult) -> bytes:
        pass

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> ParseResult:
        pass
