from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from spaghetti.cmd import run
from spaghetti.models.parse_result import ParseResult
from spaghetti.parser.source_parser import SourceParser
from spaghetti.report.implementations.console_report import ConsoleReport
from spaghetti.report.implementations.graph_report import GraphReport
from spaghetti.report.implementations.plantuml_report import PlantUMLReport
from spaghetti.result.io.implementations.file import (
    ParseResultFileReader,
    ParseResultFileWriter,
)
from spaghetti.result.serializers.interface import ParseResultSerializer


class DummySourceParser(SourceParser):
    def parse_files_from_path(self, path: Path) -> ParseResult:
        return ParseResult(module_imports={})


class DummyFileWriter(ParseResultFileWriter):
    def write(self, result: ParseResult, serializer: ParseResultSerializer) -> None:
        pass


class DummyFileReader(ParseResultFileReader):
    def read(self, serializer: ParseResultSerializer) -> ParseResult:
        return ParseResult(module_imports={})


class DummyConsoleReport(ConsoleReport):
    def render(self, result: ParseResult) -> None:
        pass


class DummyGraphReport(GraphReport):
    def render(self, result: ParseResult) -> None:
        pass


class DummyPlantUMLReport(PlantUMLReport):
    def render(self, result: ParseResult) -> None:
        pass


class TestCmd:
    @pytest.fixture
    def dummy_io(self, mocker: Any) -> None:
        mocker.patch("spaghetti.cmd.ParseResultFileReader", DummyFileReader)
        mocker.patch("spaghetti.cmd.ParseResultFileWriter", DummyFileWriter)

    def test_generate(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.SourceParser", DummySourceParser)

        runner = CliRunner()
        result = runner.invoke(run, ["generate", "-", "-"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_console(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.ConsoleReport", DummyConsoleReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-console", "-"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_graph(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.GraphReport", DummyGraphReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-dot", "-", "-"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_plantuml(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.PlantUMLReport", DummyPlantUMLReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-plantuml", "-", "-"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_max_depth(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.ConsoleReport", DummyConsoleReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-console", "-", "--max-depth", "2"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_excluded_patterns(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.ConsoleReport", DummyConsoleReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-console", "-", "--ignore", "tests"])
        assert result.exit_code == 0
        assert result.output == ""

    def test_report_filtered_patterns(self, mocker: Any, dummy_io: Any) -> None:
        mocker.patch("spaghetti.cmd.ConsoleReport", DummyConsoleReport)

        runner = CliRunner()
        result = runner.invoke(run, ["report-console", "-", "--filter", "tests"])
        assert result.exit_code == 0
        assert result.output == ""
