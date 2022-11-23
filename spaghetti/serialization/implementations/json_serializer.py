import json
from collections import OrderedDict

from spaghetti.models.module import Module
from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.serialization.interface import ProjectDependenciesSerializer


class ProjectDependenciesJsonSerializer(ProjectDependenciesSerializer):
    def serialize(self, dependencies: ProjectDependencies) -> bytes:
        json_results = OrderedDict()
        modules = sorted(dependencies.module_imports.keys())
        for module in modules:
            links = sorted(link.name for link in dependencies.module_imports[module])
            json_results[module.name] = links
        return json.dumps(json_results).encode("utf-8")

    def deserialize(self, data: bytes) -> ProjectDependencies:
        json_data = json.loads(data)
        module_imports = {}
        for source in json_data.keys():
            links = set(Module(d) for d in json_data[source])
            module_imports[Module(source)] = links
        return ProjectDependencies(module_imports=module_imports)
