import json

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultJsonSerializer(ParseResultSerializer):
    def serialize(self, result: ParseResult) -> bytes:
        json_results = {}
        for module, links in result.import_links.items():
            json_results[module.name] = [link.name for link in links]
        return json.dumps(json_results).encode("utf-8")

    def deserialize(self, data: bytes) -> ParseResult:
        json_data = json.loads(data)
        source_modules = set(Module(d) for d in json_data.keys())
        import_links = {}
        for source in json_data.keys():
            links = set(Module(d) for d in json_data[source])
            import_links[Module(source)] = links
        return ParseResult(source_modules=source_modules, import_links=import_links)
