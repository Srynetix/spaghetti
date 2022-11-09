from pathlib import Path
from typing import Optional

import click

from spaghetti.models.parse_result import ParseResult
from spaghetti.report.implementations.plantuml_report import PlantUMLReport
from spaghetti.result.io.implementations.file import (
    ParseResultFileReader,
    ParseResultFileWriter,
)

from .parser.source_parser import SourceParser
from .report.implementations.console_report import ConsoleReport
from .report.implementations.graph_report import GraphReport
from .result.filters.implementations.configurable import ConfigurableResultFilter
from .result.serializers.implementations.json_serializer import (
    ParseResultJsonSerializer,
)


@click.group()
def run():
    pass


@click.command(help="parse module links from a folder")
@click.option("--ignore", help="ignore specific paths, comma separated")
@click.argument("path", type=click.Path(path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
def parse(path: Path, output: Path, *, ignore: Optional[str] = None) -> None:
    parser = SourceParser(ignore=ignore)
    result = parser.scan_folder_recursive(path)

    serializer = ParseResultJsonSerializer()
    writer = ParseResultFileWriter(output)
    writer.write(result, serializer)


@click.command(help="report parse results in console (stdout)")
@click.option("--ignore", help="ignore specific modules")
@click.option("--filter", help="filter specific modules")
@click.option("--max-depth", help="max module depth", type=click.INT)
@click.argument("results_path", type=click.Path(path_type=Path))
def report_console(
    results_path: Path, *, max_depth: Optional[int] = None, ignore: Optional[str] = None, filter: Optional[str] = None
) -> None:
    result = _load_report(results_path, max_depth=max_depth, ignore=ignore, filter=filter)
    report = ConsoleReport()
    report.render(result)


@click.command(help="report parse results in DOT format")
@click.option("--ignore", help="ignore specific modules")
@click.option("--filter", help="filter specific modules")
@click.option("--max-depth", help="max module depth", type=click.INT)
@click.argument("results_path", type=click.Path(path_type=Path))
@click.argument("output_path", type=click.Path(path_type=Path))
def report_dot(
    results_path: Path,
    output_path: Path,
    *,
    max_depth: Optional[int] = None,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    result = _load_report(results_path, max_depth=max_depth, ignore=ignore, filter=filter)
    report = GraphReport(output_path)
    report.render(result)


@click.command(help="report parse results in PlantUML format")
@click.option("--ignore", help="ignore specific modules")
@click.option("--filter", help="filter specific modules")
@click.option("--max-depth", help="max module depth", type=click.INT)
@click.argument("results_path", type=click.Path(path_type=Path))
@click.argument("output_path", type=click.Path(path_type=Path))
def report_plantuml(
    results_path: Path,
    output_path: Path,
    *,
    max_depth: Optional[int] = None,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    result = _load_report(results_path, max_depth=max_depth, ignore=ignore, filter=filter)
    report = PlantUMLReport(output_path)
    report.render(result)


def _load_report(
    results_path: Path, *, max_depth: Optional[int], ignore: Optional[str], filter: Optional[str]
) -> ParseResult:
    excluded_patterns = [p for p in (ignore or "").split(",") if p]
    filtered_patterns = [p for p in (filter or "").split(",") if p]

    configurable_filter = ConfigurableResultFilter(
        strip_non_local_modules=True,
        hide_modules_without_links=True,
        max_depth=max_depth,
        excluded_patterns=excluded_patterns,
        filtered_patterns=filtered_patterns,
    )

    serializer = ParseResultJsonSerializer()
    reader = ParseResultFileReader(results_path)
    return configurable_filter.apply_filter(reader.read(serializer))


run.add_command(parse)
run.add_command(report_console)
run.add_command(report_dot)
run.add_command(report_plantuml)
