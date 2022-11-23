import sys

from spaghetti.models.project_dependencies import ProjectDependencies
from spaghetti.reporting.interface import Report

from .text_stream_report import TextStreamReport


class ConsoleReport(Report):
    def render(self, dependencies: ProjectDependencies) -> None:
        stream_report = TextStreamReport(sys.stdout)
        stream_report.render(dependencies)
