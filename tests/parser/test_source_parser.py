from pathlib import Path

from spaghetti.models.module import Module
from spaghetti.parser.source_parser import SourceParser

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class TestSourceParser:
    def test_parse_files(self):
        parser = SourceParser()
        result = parser.parse_files_from_path(FIXTURES_DIR)
        assert result.module_imports == {
            Module("module"): set(),
            Module("module.a"): {Module("module"), Module("module.b"), Module("sys")},
            Module("module.b"): set(),
            Module("module.c"): {Module("module"), Module("module.b")},
        }
