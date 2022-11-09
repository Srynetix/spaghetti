from pathlib import Path

from spaghetti.models.parse_result import ParseResult
from spaghetti.report.interface import Report


class PlantUMLReport(Report):
    output_path: Path

    def __init__(self, output: Path) -> None:
        self.output_path = output

    def render(self, result: ParseResult) -> None:
        code = "@startuml\n\n"

        modules = sorted(result.import_links.keys())
        for module in modules:
            sorted_deps = sorted(result.import_links[module])
            for dep in sorted_deps:
                code += f"[{module.name}] --> [{dep.name}]\n"

        code += "@enduml"

        with open(self.output_path, mode="w", encoding="utf-8") as hndl:
            hndl.write(code)
