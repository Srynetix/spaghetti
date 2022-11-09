from pathlib import Path

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.io.implementations.stream import (
    ParseResultStreamReader,
    ParseResultStreamWriter,
)
from spaghetti.result.io.interfaces import ParseResultReader, ParseResultWriter
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultFileWriter(ParseResultWriter):
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, result: ParseResult, serializer: ParseResultSerializer) -> None:
        with open(self.path, mode="w", encoding="utf-8") as fd:
            writer = ParseResultStreamWriter(fd)
            writer.write(result, serializer)


class ParseResultFileReader(ParseResultReader):
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self, serializer: ParseResultSerializer) -> ParseResult:
        with open(self.path, mode="r", encoding="utf-8") as fd:
            reader = ParseResultStreamReader(fd)
            return reader.read(serializer)
