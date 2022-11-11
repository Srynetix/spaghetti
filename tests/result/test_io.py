from pathlib import Path
from typing import Any

from spaghetti.models.parse_result import ParseResult
from spaghetti.result.io.implementations.file import (
    ParseResultFileReader,
    ParseResultFileWriter,
)
from spaghetti.result.serializers.interface import ParseResultSerializer


class DummySerializer(ParseResultSerializer):
    source: ParseResult

    def __init__(self, source: ParseResult) -> None:
        self.source = source

    def serialize(self, result: ParseResult) -> bytes:
        return b"serialized"

    def deserialize(self, data: bytes) -> ParseResult:
        return self.source


class TestFileIO:
    def test_write(self, sample_parse_result: ParseResult, tmpdir: Any) -> None:
        target_file = Path(tmpdir.join("file.dat"))
        serializer = DummySerializer(sample_parse_result)

        writer = ParseResultFileWriter(target_file)
        writer.write(sample_parse_result, serializer)
        assert target_file.read_bytes() == b"serialized"

    def test_read(self, sample_parse_result: ParseResult, tmpdir: Any) -> None:
        target_file = Path(tmpdir.join("file.dat"))
        target_file.write_bytes(b"serialize")
        serializer = DummySerializer(sample_parse_result)

        reader = ParseResultFileReader(target_file)
        assert reader.read(serializer) == sample_parse_result
