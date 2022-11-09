from typing import IO, Any

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.io.interfaces import ParseResultReader, ParseResultWriter
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultStreamWriter(ParseResultWriter):
    stream: IO[Any]

    def __init__(self, stream: IO[Any]) -> None:
        self.stream = stream

    def write(self, result: ParseResult, serializer: ParseResultSerializer) -> None:
        self.stream.write(serializer.serialize(result).decode("utf-8"))


class ParseResultStreamReader(ParseResultReader):
    stream: IO[Any]

    def __init__(self, stream: IO[Any]) -> None:
        self.stream = stream

    def read(self, serializer: ParseResultSerializer) -> ParseResult:
        return serializer.deserialize(self.stream.read())
