from pathlib import Path
from typing import Any

from spaghetti.models.parse_result import ParseResult
from spaghetti.report.implementations.console_report import ConsoleReport
from spaghetti.report.implementations.graph_report import GraphReport
from spaghetti.report.implementations.plantuml_report import PlantUMLReport


class TestConsoleReport:
    def test_report(self, sample_parse_result: ParseResult) -> None:
        report = ConsoleReport()
        report.render(sample_parse_result)


class TestGraphReport:
    def test_report(self, sample_parse_result: ParseResult, tmpdir: Any) -> None:
        output_path = Path(tmpdir.join("test.dot"))
        report = GraphReport(output_path)
        report.render(sample_parse_result)
        assert (
            output_path.read_text()
            == """digraph G {
"module.a" -> "module.b"
"module.a" -> "sys"
"module.c" -> "module.b"
}"""
        )


class TestPlantUMLReport:
    def test_report(self, sample_parse_result: ParseResult, tmpdir: Any) -> None:
        output_path = Path(tmpdir.join("test.plantuml"))
        report = PlantUMLReport(output_path)
        report.render(sample_parse_result)
        assert (
            output_path.read_text()
            == """@startuml

[module.a] --> [module.b]
[module.a] --> [sys]
[module.c] --> [module.b]
@enduml"""
        )
