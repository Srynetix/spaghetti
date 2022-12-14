import functools
from pathlib import Path
from typing import Any, Callable, Optional

import click

from spaghetti.filtering.implementations.configurable import ConfigurableFilter
from spaghetti.io.implementations.file import (
    ProjectDependenciesFileReader,
    ProjectDependenciesFileWriter,
)
from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.parsing.source_parser import SourceParser
from spaghetti.reporting.implementations.console_report import ConsoleReport
from spaghetti.reporting.implementations.graph_report import GraphReport
from spaghetti.reporting.implementations.plantuml_report import PlantUMLReport
from spaghetti.serialization.implementations.json_serializer import (
    ProjectDependenciesJsonSerializer,
)


def setup_filter_arguments(fn: Callable[..., Any]) -> Callable[..., Any]:
    @click.option("--ignore", help="ignore specific modules (comma separated strings)")
    @click.option("--filter", help="filter specific modules (comma separated strings)")
    @click.option("--max-depth", help="max module depth", type=click.INT, default=0)
    @click.argument("results_path", type=click.Path(path_type=Path))
    @functools.wraps(fn)
    def inner(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    return inner


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def run() -> None:
    """
    trace your Python module dependencies to have a better picture before cleaning!
    """


@click.command()
@click.argument("path", type=click.Path(path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
def generate(path: Path, output: Path) -> None:
    """
    generate a module parsing result file
    """
    parser = SourceParser()
    result = parser.parse_files_from_path(path)

    serializer = ProjectDependenciesJsonSerializer()
    writer = ProjectDependenciesFileWriter(output)
    writer.write(result, serializer)


@click.command()
@setup_filter_arguments
def report_console(
    results_path: Path,
    *,
    max_depth: int = 0,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    """
    report a module parsing result file in console (stdout)
    """
    result = _load_report(
        results_path, max_depth=max_depth, excluded_patterns=ignore, filtered_patterns=filter
    )
    report = ConsoleReport()
    report.render(result)


@click.command()
@setup_filter_arguments
@click.argument("output_path", type=click.Path(path_type=Path))
def report_dot(
    results_path: Path,
    output_path: Path,
    *,
    max_depth: int = 0,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    """
    report a module parsing result file in DOT format

    pass - as OUTPUT_PATH to print to stdout
    """
    result = _load_report(
        results_path, max_depth=max_depth, excluded_patterns=ignore, filtered_patterns=filter
    )
    report = GraphReport(output_path)
    report.render(result)


@click.command()
@setup_filter_arguments
@click.argument("output_path", type=click.Path(path_type=Path))
def report_plantuml(
    results_path: Path,
    output_path: Path,
    *,
    max_depth: int = 0,
    ignore: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    """
    report a module parsing result file in PlantUML format

    pass - as OUTPUT_PATH to print to stdout
    """
    result = _load_report(
        results_path, max_depth=max_depth, excluded_patterns=ignore, filtered_patterns=filter
    )
    report = PlantUMLReport(output_path)
    report.render(result)


def _load_report(
    results_path: Path,
    *,
    max_depth: Optional[int],
    excluded_patterns: Optional[str],
    filtered_patterns: Optional[str],
) -> ProjectDependencies:
    excluded_patterns_set = {p for p in (excluded_patterns or "").split(",") if p}
    filtered_patterns_set = {p for p in (filtered_patterns or "").split(",") if p}

    serializer = ProjectDependenciesJsonSerializer()
    reader = ProjectDependenciesFileReader(results_path)
    dependencies = reader.read(serializer)

    configurable_filter = ConfigurableFilter(
        excluded_patterns=excluded_patterns_set,
        filtered_patterns=filtered_patterns_set,
        max_depth=max_depth or 0,
    )

    return configurable_filter.apply_filter(dependencies)


run.add_command(generate)
run.add_command(report_console)
run.add_command(report_dot)
run.add_command(report_plantuml)
