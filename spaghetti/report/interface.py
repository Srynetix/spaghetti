from abc import ABC, abstractmethod

from spaghetti.models.parse_result import ParseResult


class Report(ABC):
    @abstractmethod
    def render(self, result: ParseResult) -> None:
        """Render the report."""
