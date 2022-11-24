# spaghetti :spaghetti:

[![Coverage Status](https://coveralls.io/repos/github/Srynetix/spaghetti/badge.svg?branch=main)](https://coveralls.io/github/Srynetix/spaghetti?branch=main)

Trace your Python module dependencies to have a better picture before cleaning!

You can find a web app around **spaghetti** here: [spaghetti-ui](https://github.com/Srynetix/spaghetti-ui)

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
spaghetti.cmd (dependencies: 8, reverse dependencies: 1):
  - spaghetti.filtering.implementations.configurable
  - spaghetti.io.implementations.file
  - spaghetti.models.project_dependencies
  - spaghetti.parsing.source_parser
  - spaghetti.reporting.implementations.console_report
  - spaghetti.reporting.implementations.graph_report
  - spaghetti.reporting.implementations.plantuml_report
  - spaghetti.serialization.implementations.json_serializer
spaghetti.filtering.implementations.chain (dependencies: 2, reverse dependencies: 2):
  - spaghetti.filtering.interface
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.configurable (dependencies: 8, reverse dependencies: 1):
  - spaghetti.filtering.implementations.chain
  - spaghetti.filtering.implementations.exclude_patterns
  - spaghetti.filtering.implementations.filter_patterns
  - spaghetti.filtering.implementations.hide_modules_without_links
  - spaghetti.filtering.implementations.limit_max_depth
  - spaghetti.filtering.implementations.strip_non_local_modules
  - spaghetti.filtering.interface
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.exclude_patterns (dependencies: 4, reverse dependencies: 2):
  - spaghetti.filtering.interface
  - spaghetti.log
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.filter_patterns (dependencies: 4, reverse dependencies: 3):
  - spaghetti.filtering.interface
  - spaghetti.log
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.hide_modules_without_links (dependencies: 2, reverse dependencies: 2):
  - spaghetti.filtering.interface
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.limit_max_depth (dependencies: 3, reverse dependencies: 2):
  - spaghetti.filtering.interface
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.filtering.implementations.strip_non_local_modules (dependencies: 3, reverse dependencies: 2):
  - spaghetti.filtering.interface
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.filtering.interface (dependencies: 1, reverse dependencies: 7):
  - spaghetti.models.project_dependencies
spaghetti.io.implementations.file (dependencies: 4, reverse dependencies: 3):
  - spaghetti.io.implementations.stream
  - spaghetti.io.interfaces
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.interface
spaghetti.io.implementations.stream (dependencies: 3, reverse dependencies: 1):
  - spaghetti.io.interfaces
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.interface
spaghetti.io.interfaces (dependencies: 2, reverse dependencies: 2):
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.interface
spaghetti.models.project_dependencies (dependencies: 1, reverse dependencies: 32):
  - spaghetti.models.module
spaghetti.parsing.import_node_visitor (dependencies: 1, reverse dependencies: 1):
  - spaghetti.parsing.import_declaration
spaghetti.parsing.module_resolver (dependencies: 3, reverse dependencies: 2):
  - spaghetti.log
  - spaghetti.models.module
  - spaghetti.parsing.import_declaration
spaghetti.parsing.source_parser (dependencies: 6, reverse dependencies: 3):
  - spaghetti.log
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
  - spaghetti.parsing.import_declaration
  - spaghetti.parsing.import_node_visitor
  - spaghetti.parsing.module_resolver
spaghetti.reporting.implementations.console_report (dependencies: 3, reverse dependencies: 3):
  - spaghetti.models.project_dependencies
  - spaghetti.reporting.implementations.text_stream_report
  - spaghetti.reporting.interface
spaghetti.reporting.implementations.graph_report (dependencies: 2, reverse dependencies: 3):
  - spaghetti.models.project_dependencies
  - spaghetti.reporting.interface
spaghetti.reporting.implementations.plantuml_report (dependencies: 2, reverse dependencies: 3):
  - spaghetti.models.project_dependencies
  - spaghetti.reporting.interface
spaghetti.reporting.implementations.text_stream_report (dependencies: 2, reverse dependencies: 1):
  - spaghetti.models.project_dependencies
  - spaghetti.reporting.interface
spaghetti.reporting.interface (dependencies: 1, reverse dependencies: 4):
  - spaghetti.models.project_dependencies
spaghetti.serialization.implementations.json_serializer (dependencies: 3, reverse dependencies: 2):
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.interface
spaghetti.serialization.interface (dependencies: 1, reverse dependencies: 6):
  - spaghetti.models.project_dependencies
spaghetti.tests.conftest (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_chain (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.chain
  - spaghetti.filtering.implementations.filter_patterns
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_exclude_patterns (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.exclude_patterns
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_filter_patterns (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.filter_patterns
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_hide_modules_without_links (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.hide_modules_without_links
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_limit_max_depth (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.limit_max_depth
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.filtering.test_strip_non_local_modules (dependencies: 3, reverse dependencies: 0):
  - spaghetti.filtering.implementations.strip_non_local_modules
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.models.test_module (dependencies: 1, reverse dependencies: 0):
  - spaghetti.models.module
spaghetti.tests.models.test_project_dependencies (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
spaghetti.tests.parsing.test_import_declaration (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parsing.import_declaration
spaghetti.tests.parsing.test_module_resolver (dependencies: 3, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.parsing.import_declaration
  - spaghetti.parsing.module_resolver
spaghetti.tests.parsing.test_source_parser (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.module
  - spaghetti.parsing.source_parser
spaghetti.tests.reporting.test_reports (dependencies: 4, reverse dependencies: 0):
  - spaghetti.models.project_dependencies
  - spaghetti.reporting.implementations.console_report
  - spaghetti.reporting.implementations.graph_report
  - spaghetti.reporting.implementations.plantuml_report
spaghetti.tests.test_cmd (dependencies: 8, reverse dependencies: 0):
  - spaghetti.cmd
  - spaghetti.io.implementations.file
  - spaghetti.models.project_dependencies
  - spaghetti.parsing.source_parser
  - spaghetti.reporting.implementations.console_report
  - spaghetti.reporting.implementations.graph_report
  - spaghetti.reporting.implementations.plantuml_report
  - spaghetti.serialization.interface
spaghetti.tests.test_io (dependencies: 3, reverse dependencies: 0):
  - spaghetti.io.implementations.file
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.interface
spaghetti.tests.test_serializers (dependencies: 2, reverse dependencies: 0):
  - spaghetti.models.project_dependencies
  - spaghetti.serialization.implementations.json_serializer
```

### Show a console report of a result file, limiting the module depth to 2, excluding tests

    spaghetti report-console results.json --max-depth 2 --ignore tests

You can pass options to the report commands (they should be the same for each report command).
Here's the result:

```
spaghetti.cmd (dependencies: 6, reverse dependencies: 0):
  - spaghetti.filtering
  - spaghetti.io
  - spaghetti.models
  - spaghetti.parsing
  - spaghetti.reporting
  - spaghetti.serialization
spaghetti.filtering (dependencies: 2, reverse dependencies: 1):
  - spaghetti.log
  - spaghetti.models
spaghetti.io (dependencies: 2, reverse dependencies: 1):
  - spaghetti.models
  - spaghetti.serialization
spaghetti.parsing (dependencies: 2, reverse dependencies: 1):
  - spaghetti.log
  - spaghetti.models
spaghetti.reporting (dependencies: 1, reverse dependencies: 1):
  - spaghetti.models
spaghetti.serialization (dependencies: 1, reverse dependencies: 2):
  - spaghetti.models
```

### Show a console report of a result file, focusing on a specific module

    spaghetti report-console results.json --filter spaghetti.parsing.source_parser

It can be useful to focus on specific modules.

```
spaghetti.cmd (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parsing.source_parser
spaghetti.parsing.source_parser (dependencies: 6, reverse dependencies: 3):
  - spaghetti.log
  - spaghetti.models.module
  - spaghetti.models.project_dependencies
  - spaghetti.parsing.import_declaration
  - spaghetti.parsing.import_node_visitor
  - spaghetti.parsing.module_resolver
spaghetti.tests.parsing.test_source_parser (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parsing.source_parser
spaghetti.tests.test_cmd (dependencies: 1, reverse dependencies: 0):
  - spaghetti.parsing.source_parser
```

Make sure to try these using other "report" commands!
