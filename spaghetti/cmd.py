import functools
import logging
from pathlib import Path
from typing import Optional, Set

import click
import structlog

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.report.implementations.plantuml_report import PlantUMLReport
from spaghetti.result.io.implementations.file import (
    ParseResultFileReader,
    ParseResultFileWriter,
)

from .parser.source_parser import SourceParser
from .report.implementations.console_report import ConsoleReport
from .report.implementations.graph_report import GraphReport
from .result.filters.chain import ResultFilterChain
from .result.filters.implementations.exclude_patterns import ExcludePatternsResultFilter
from .result.filters.implementations.filter_patterns import FilterPatternsResultFilter
from .result.filters.implementations.hide_modules_without_links import (
    HideModulesWithoutLinksResultFilter,
)
from .result.filters.implementations.limit_max_depth import LimitMaxDepthResultFilter
from .result.filters.implementations.strip_non_local_modules import (
    StripNonLocalModulesResultFilter,
)
from .result.serializers.implementations.json_serializer import (
    ParseResultJsonSerializer,
)

# Only shows INFO+ messages
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)


def setup_filter_arguments(fn):
    @click.option("--ignore", help="ignore specific modules (comma separated strings)")
    @click.option("--filter", help="filter specific modules (comma separated strings)")
    @click.option("--max-depth", help="max module depth", type=click.INT)
    @click.argument("results_path", type=click.Path(path_type=Path))
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)

    return inner


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def run():
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

    serializer = ParseResultJsonSerializer()
    writer = ParseResultFileWriter(output)
    writer.write(result, serializer)


@click.command()
@setup_filter_arguments
def report_console(
    results_path: Path,
    *,
    max_depth: Optional[int] = None,
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
    max_depth: Optional[int] = None,
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
    max_depth: Optional[int] = None,
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
) -> ParseResult:
    excluded_patterns_set = {p for p in (excluded_patterns or "").split(",") if p}
    filtered_patterns_set = {p for p in (filtered_patterns or "").split(",") if p}

    serializer = ParseResultJsonSerializer()
    reader = ParseResultFileReader(results_path)
    result = reader.read(serializer)

    return _build_filter_chain(
        local_modules=set(result.module_imports.keys()),
        max_depth=max_depth,
        excluded_patterns=excluded_patterns_set,
        filtered_patterns=filtered_patterns_set,
    ).apply_filter(result)


def _build_filter_chain(
    *,
    local_modules: Set[Module],
    max_depth: Optional[int],
    excluded_patterns: Set[str],
    filtered_patterns: Set[str],
) -> ResultFilterChain:
    filters = []

    if max_depth:
        filters.append(LimitMaxDepthResultFilter(max_depth))
    if excluded_patterns:
        filters.append(ExcludePatternsResultFilter(excluded_patterns))
    if filtered_patterns:
        filters.append(FilterPatternsResultFilter(filtered_patterns))

    filters.extend(
        (
            StripNonLocalModulesResultFilter(local_modules),
            HideModulesWithoutLinksResultFilter(),
        )
    )

    return ResultFilterChain(filters)


run.add_command(generate)
run.add_command(report_console)
run.add_command(report_dot)
run.add_command(report_plantuml)
