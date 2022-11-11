import ast
import os
from pathlib import Path
from typing import Dict, Set

from structlog import get_logger

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult
from spaghetti.parser.module_resolver import ModuleResolver

from .import_declaration import ImportDeclaration
from .import_node_visitor import ImportNodeVisitor


class SourceParser:
    known_local_modules: Set[Module]

    def __init__(self) -> None:
        self.logger = get_logger("SourceParser")
        self.known_local_modules = set()

    def parse_files_from_path(self, root_path: Path) -> ParseResult:
        source_file_paths = self._scan_files_in_folder_recursive(root_path)
        self.known_local_modules = self._compute_known_local_modules(root_path, source_file_paths)

        module_imports: Dict[Module, Set[Module]] = {}
        for source_file_path in source_file_paths:
            source_module = Module.from_path(root_path, source_file_path)
            imports = self._read_module_imports_in_file(root_path, source_file_path)
            self.logger.debug("module_imports", source_module=source_module, imports=module_imports)
            module_imports[source_module] = imports

        return ParseResult(module_imports=module_imports)

    def _scan_files_in_folder_recursive(self, root_path: Path) -> Set[Path]:
        source_files = set()

        for root, folders, files in os.walk(root_path):
            if "node_modules" in folders:
                folders.remove("node_modules")

            for source_file in files:
                if source_file.endswith(".py"):
                    full_path = Path(os.path.join(root, source_file))
                    source_files.add(full_path)

        return source_files

    def _compute_known_local_modules(
        self, root_path: Path, source_file_paths: Set[Path]
    ) -> Set[Module]:
        known_local_modules = set()
        for source_file_path in source_file_paths:
            source_module = Module.from_path(root_path, source_file_path)
            known_local_modules.add(source_module)

        return known_local_modules

    def _read_module_imports_in_file(self, root_path: Path, source_file_path: Path) -> Set[Module]:
        source_module = Module.from_path(root_path, source_file_path)
        file_contents = self._read_source_file(source_file_path)
        import_declarations = self._scan_imports_from_source_file(source_file_path, file_contents)

        resolver = ModuleResolver(self.known_local_modules)
        modules = resolver.convert_import_declarations_to_modules(
            source_module, import_declarations
        )

        self.logger.debug(
            "imports_scanned", source_file=source_file_path, module=source_module, modules=modules
        )
        return modules

    def _read_source_file(self, source_file_path: Path) -> str:
        with open(source_file_path, mode="r", encoding="utf-8") as fd:
            return fd.read()

    def _scan_imports_from_source_file(
        self, source_file_path: Path, source_file_contents: str
    ) -> Set[ImportDeclaration]:
        tree = ast.parse(source_file_contents, str(source_file_path))
        visitor = ImportNodeVisitor()
        visitor.visit(tree)
        return visitor.declarations
