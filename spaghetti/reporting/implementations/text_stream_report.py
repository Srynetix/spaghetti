from typing import IO

from rich import print as rich_print

from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.reporting.interface import Report


class TextStreamReport(Report):
    def __init__(self, stream: IO[str]) -> None:
        self.stream = stream

    def render(self, dependencies: ProjectDependencies) -> None:
        modules = sorted(dependencies.module_imports.keys())
        for module in modules:
            sorted_deps = sorted(dependencies.module_imports[module])
            dependency_count = dependencies.get_module_dependency_count(module)
            reverse_dependency_count = dependencies.get_module_reverse_dependency_count(module)
            rich_print(
                f"[bold]{module.name} (dependencies: {dependency_count}, "
                f"reverse dependencies: {reverse_dependency_count}):[/bold]",
                file=self.stream,
            )
            for dep in sorted_deps:
                rich_print(f"  - {dep.name}", file=self.stream)
