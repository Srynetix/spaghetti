from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.hide_modules_without_links import (
    HideModulesWithoutLinksResultFilter,
)


class TestHideModulesWithoutLinksResultFilter:
    def test_filter(self, sample_parse_result: ParseResult) -> None:
        filt = HideModulesWithoutLinksResultFilter()
        assert filt.apply_filter(sample_parse_result) == ParseResult(
            module_imports={
                Module("module.a"): {Module("sys"), Module("module.b")},
                Module("module.c"): {Module("module.b")},
            }
        )
