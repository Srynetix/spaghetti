from spaghetti.models.parse_result import ParseResult
from spaghetti.result.serializers.implementations.json_serializer import (
    ParseResultJsonSerializer,
)


class TestJsonSerializer:
    def test_serialize(self, sample_parse_result: ParseResult) -> None:
        serializer = ParseResultJsonSerializer()
        assert (
            serializer.serialize(sample_parse_result)
            == b'{"module.a": ["module.b", "sys"], "module.b": [], "module.c": ["module.b"]}'
        )

    def test_deserialize(self, sample_parse_result: ParseResult) -> None:
        serializer = ParseResultJsonSerializer()
        assert (
            serializer.deserialize(
                b'{"module.a": ["module.b", "sys"], "module.b": [], "module.c": ["module.b"]}'
            )
            == sample_parse_result
        )
