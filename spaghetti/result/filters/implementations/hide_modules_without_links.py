from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.interface import ParseResultFilter


class HideModulesWithoutLinksResultFilter(ParseResultFilter):
    def apply_filter(self, result: ParseResult) -> ParseResult:
        return ParseResult(
            module_imports={
                module: links for module, links in result.module_imports.items() if len(links) > 0
            }
        )
