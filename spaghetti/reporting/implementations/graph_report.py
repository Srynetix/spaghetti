from pathlib import Path

from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.reporting.interface import Report


class GraphReport(Report):
    output_path: Path

    def __init__(self, output: Path) -> None:
        self.output_path = output

    def render(self, dependencies: ProjectDependencies) -> None:
        code = "digraph G {\n"

        modules = sorted(dependencies.module_imports.keys())
        for module in modules:
            sorted_deps = sorted(dependencies.module_imports[module])
            for dep in sorted_deps:
                code += f'"{module.name}" -> "{dep.name}"\n'

        code += "}"

        if self.output_path == Path("-"):
            print(code)
        else:
            with open(self.output_path, mode="w", encoding="utf-8") as hndl:
                hndl.write(code)
