# spaghetti

[![Coverage Status](https://coveralls.io/repos/github/Srynetix/spaghetti/badge.svg?branch=main)](https://coveralls.io/github/Srynetix/spaghetti?branch=main)

Trace your Python module dependencies to have a better picture before cleaning!

## Requirements

- Python 3.9+
- Poetry

## How to build

You need to build a wheel/zip using Poetry, then you can install it globally using `pip`.

    poetry build
    pip install ./dist/spaghetti*.whl

## How to use

The `spaghetti` command-line needs two steps:
- First, the generation step with the `generate` command
- Then, the reporting step with the multiple `report` commands:
    - `report-console`: to display results in the console
    - `report-dot`: to generate a GraphViz file
    - `report-plantuml`: to generate a PlantUML file

### Generate dependency result file for a specific Python project

    spaghetti generate ./your/project/path results.json

This will generate a module dependency result file that you can exploit using one of the "report" commands.

### Show a console report of a result file

    spaghetti report-console result.json

When executing this command on the spaghetti repository, here's the result:

```
spaghetti.cmd (dependencies: 13, reverse dependencies: 0):
  - spaghetti.models.parse_result
  - spaghetti.parser.source_parser
  - spaghetti.report.implementations.console_report
  - spaghetti.report.implementations.graph_report
  - spaghetti.report.implementations.plantuml_report
  - spaghetti.result.filters.chain
  - spaghetti.result.filters.implementations.exclude_patterns
  - spaghetti.result.filters.implementations.filter_patterns
  - spaghetti.result.filters.implementations.hide_modules_without_links
  - spaghetti.result.filters.implementations.limit_max_depth
  - spaghetti.result.filters.implementations.strip_non_local_modules
  - spaghetti.result.io.implementations.file
  - spaghetti.result.serializers.implementations.json_serializer
spaghetti.models.parse_result (dependencies: 1, reverse dependencies: 29):
  - spaghetti.models.module
spaghetti.parser.import_node_visitor (dependencies: 1, reverse dependencies: 1):
  - spaghetti.parser.import_declaration
spaghetti.parser.module_resolver (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.parser.import_declaration
spaghetti.parser.source_parser (dependencies: 5, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.parser.import_declaration
  - spaghetti.parser.import_node_visitor
  - spaghetti.parser.module_resolver
spaghetti.report.implementations.console_report (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.report.interface
spaghetti.report.implementations.graph_report (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.report.interface
spaghetti.report.implementations.plantuml_report (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.report.interface
spaghetti.report.interface (dependencies: 1, reverse dependencies: 3):
  - spaghetti.models.parse_result
spaghetti.result.filters.chain (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.implementations.exclude_patterns (dependencies: 3, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.implementations.filter_patterns (dependencies: 3, reverse dependencies: 3):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.implementations.hide_modules_without_links (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.implementations.limit_max_depth (dependencies: 3, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.implementations.strip_non_local_modules (dependencies: 3, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.interface
spaghetti.result.filters.interface (dependencies: 1, reverse dependencies: 6):
  - spaghetti.models.parse_result
spaghetti.result.io.implementations.file (dependencies: 4, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.result.io.implementations.stream
  - spaghetti.result.io.interfaces
  - spaghetti.result.serializers.interface
spaghetti.result.io.implementations.stream (dependencies: 3, reverse dependencies: 1):
  - spaghetti.models.parse_result
  - spaghetti.result.io.interfaces
  - spaghetti.result.serializers.interface
spaghetti.result.io.interfaces (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.parse_result
  - spaghetti.result.serializers.interface
spaghetti.result.serializers.implementations.json_serializer (dependencies: 3, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.serializers.interface
spaghetti.result.serializers.interface (dependencies: 1, reverse dependencies: 5):
  - spaghetti.models.parse_result
tests.conftest (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
tests.models.test_module (dependencies: 1, reverse dependencies: 0):
  - spaghetti.models.module
tests.models.test_parse_result (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
tests.parser.test_import_declaration (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parser.import_declaration
tests.parser.test_module_resolver (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.parser.import_declaration
  - spaghetti.parser.module_resolver
tests.parser.test_source_parser (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.parser.source_parser
tests.report.test_reports (dependencies: 4, reverse dependencies: 0):
  - spaghetti.models.parse_result
  - spaghetti.report.implementations.console_report
  - spaghetti.report.implementations.graph_report
  - spaghetti.report.implementations.plantuml_report
tests.result.filters.test_chain (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.parse_result
  - spaghetti.result.filters.chain
  - spaghetti.result.filters.implementations.filter_patterns
tests.result.filters.test_exclude_patterns (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.implementations.exclude_patterns
tests.result.filters.test_filter_patterns (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.implementations.filter_patterns
tests.result.filters.test_hide_modules_without_links (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.implementations.hide_modules_without_links
tests.result.filters.test_limit_max_depth (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.implementations.limit_max_depth
tests.result.filters.test_strip_non_local_modules (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.result.filters.implementations.strip_non_local_modules
tests.result.test_io (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.parse_result
  - spaghetti.result.io.implementations.file
  - spaghetti.result.serializers.interface
tests.result.test_serializers (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.parse_result
  - spaghetti.result.serializers.implementations.json_serializer
```

### Show a console report of a result file, limiting the module depth to 2, excluding tests

    spaghetti report-console results.json --max-depth 2 --ignore tests

You can pass options to the report commands (they should be the same for each report command).
Here's the result:

```
spaghetti.cmd (dependencies: 4, reverse dependencies: 0):
  - spaghetti.models
  - spaghetti.parser
  - spaghetti.report
  - spaghetti.result
spaghetti.parser (dependencies: 1, reverse dependencies: 1):
  - spaghetti.models
spaghetti.report (dependencies: 1, reverse dependencies: 1):
  - spaghetti.models
spaghetti.result (dependencies: 1, reverse dependencies: 1):
  - spaghetti.models
```

### Show a console report of a result file, focusing on a specific module

    spaghetti report-console results.json --filter spaghetti.parser.source_parser

It can be useful to focus on specific modules.

```
paghetti.cmd (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parser.source_parser
spaghetti.parser.source_parser (dependencies: 5, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.parse_result
  - spaghetti.parser.import_declaration
  - spaghetti.parser.import_node_visitor
  - spaghetti.parser.module_resolver
tests.parser.test_source_parser (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parser.source_parser
```

Make sure to try these using other "report" commands!