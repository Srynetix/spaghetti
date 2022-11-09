import logging
from pathlib import Path
from typing import Optional

import click
import structlog

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

# Only shows INFO+ messages
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def run():
    """
    Trace your Python module dependencies to have a better picture before cleaning!
    """


@click.command(help="generate a module parsing result file")
@click.option("--ignore", help="ignore specific paths, comma separated")
@click.argument("path", type=click.Path(path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
def generate(path: Path, output: Path, *, ignore: Optional[str] = None) -> None:
    parser = SourceParser(ignore=ignore)
    result = parser.parse_files_from_path(path)

    serializer = ParseResultJsonSerializer()
    writer = ParseResultFileWriter(output)
    writer.write(result, serializer)


@click.command(help="report a module parsing result file in console (stdout)")
@click.option("--ignore", help="ignore specific modules")
@click.option("--filter", help="filter specific modules")
@click.option("--max-depth", help="max module depth", type=click.INT)
@click.argument("results_path", type=click.Path(path_type=Path))
def report_console(
    results_path: Path,
    *,
    max_depth: Optional[int] = None,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    result = _load_report(results_path, max_depth=max_depth, ignore=ignore, filter=filter)
    report = ConsoleReport()
    report.render(result)


@click.command(help="report a module parsing result file in DOT format")
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


@click.command(help="report a module parsing result file in PlantUML format")
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


run.add_command(generate)
run.add_command(report_console)
run.add_command(report_dot)
run.add_command(report_plantuml)
