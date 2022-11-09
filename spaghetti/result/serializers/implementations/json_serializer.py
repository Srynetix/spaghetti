import json
from collections import OrderedDict

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.serializers.interface import ParseResultSerializer


class ParseResultJsonSerializer(ParseResultSerializer):
    def serialize(self, result: ParseResult) -> bytes:
        json_results = OrderedDict()
        modules = sorted(result.module_imports.keys())
        for module in modules:
            links = sorted(link.name for link in result.module_imports[module])
            json_results[module.name] = links
        return json.dumps(json_results).encode("utf-8")

    def deserialize(self, data: bytes) -> ParseResult:
        json_data = json.loads(data)
        module_imports = {}
        for source in json_data.keys():
            links = set(Module(d) for d in json_data[source])
            module_imports[Module(source)] = links
        return ParseResult(module_imports=module_imports)
