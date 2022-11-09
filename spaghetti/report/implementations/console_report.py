from rich import print as rich_print

from spaghetti.models.parse_result import ParseResult
from spaghetti.report.interface import Report


class ConsoleReport(Report):
    def render(self, result: ParseResult) -> None:
        modules = sorted(result.module_imports.keys())
        for module in modules:
            sorted_deps = sorted(result.module_imports[module])
            dependency_count = result.get_module_dependency_count(module)
            reverse_dependency_count = result.get_module_reverse_dependency_count(module)
            rich_print(
                f"[bold]{module.name} (dependencies: {dependency_count}, "
                f"reverse dependencies: {reverse_dependency_count}):[/bold]"
            )
            for dep in sorted_deps:
                rich_print(f"  - {dep.name}")
