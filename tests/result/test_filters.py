from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.result.filters.implementations.configurable import (
    ConfigurableResultFilter,
)


class TestConfigurableFilter:
    def test_empty_filter(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter()
        assert conf_filter.apply_filter(sample_parse_result) == sample_parse_result

    def test_exclude(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(excluded_patterns=["module.a"])
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.b"): set(), Module("module.c"): {Module("module.b")}}
        )

    def test_exclude_link(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(excluded_patterns=["module.b"])
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.a"): {Module("sys")}, Module("module.c"): set()}
        )

    def test_filter(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(filtered_patterns=["module.a"])
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module.a"): {Module("sys"), Module("module.b")}}
        )

    def test_depth(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(max_depth=1)
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={Module("module"): {Module("sys")}}
        )

    def test_hide_modules_without_links(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(hide_modules_without_links=True)
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={
                Module("module.a"): {Module("sys"), Module("module.b")},
                Module("module.c"): {Module("module.b")},
            }
        )

    def test_strip_non_local_modules(self, sample_parse_result: ParseResult):
        conf_filter = ConfigurableResultFilter(strip_non_local_modules=True)
        assert conf_filter.apply_filter(sample_parse_result) == ParseResult(
            module_imports={
                Module("module.a"): {Module("module.b")},
                Module("module.b"): set(),
                Module("module.c"): {Module("module.b")},
            }
        )
