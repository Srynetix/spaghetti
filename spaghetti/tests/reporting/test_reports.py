from pathlib import Path
from typing import Any

from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.reporting.implementations.console_report import ConsoleReport
from spaghetti.reporting.implementations.graph_report import GraphReport
from spaghetti.reporting.implementations.plantuml_report import PlantUMLReport


class TestConsoleReport:
    def test_report(self, sample_dependencies: ProjectDependencies) -> None:
        report = ConsoleReport()
        report.render(sample_dependencies)


class TestGraphReport:
    def test_report(self, sample_dependencies: ProjectDependencies, tmpdir: Any) -> None:
        output_path = Path(tmpdir.join("test.dot"))
        report = GraphReport(output_path)
        report.render(sample_dependencies)
        assert (
            output_path.read_text()
            == """digraph G {
"module.a" -> "module.b"
"module.a" -> "sys"
"module.c" -> "module.b"
}"""
        )

    def test_report_stdout(self, sample_dependencies: ProjectDependencies) -> None:
        report = GraphReport(Path("-"))
        report.render(sample_dependencies)


class TestPlantUMLReport:
    def test_report(self, sample_dependencies: ProjectDependencies, tmpdir: Any) -> None:
        output_path = Path(tmpdir.join("test.plantuml"))
        report = PlantUMLReport(output_path)
        report.render(sample_dependencies)
        assert (
            output_path.read_text()
            == """@startuml

[module.a] --> [module.b]
[module.a] --> [sys]
[module.c] --> [module.b]

@enduml"""
        )

    def test_report_stdout(self, sample_dependencies: ProjectDependencies) -> None:
        report = PlantUMLReport(Path("-"))
        report.render(sample_dependencies)
