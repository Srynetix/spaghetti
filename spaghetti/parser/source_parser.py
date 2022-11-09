import ast
import os
from pathlib import Path
from re import Match
from typing import Dict, List, Optional, Set

from structlog import get_logger

from spaghetti.models.module import Module
from spaghetti.models.parse_result import ParseResult

from .import_declaration import ImportDeclaration
from .import_node_visitor import ImportNodeVisitor


class SourceParser:
    ignore: List[str]
    known_local_modules: Set[Module]

    def __init__(self, *, ignore: Optional[str] = None):
        self.logger = get_logger("SourceParser")
        self.known_local_modules = set()

        if ignore:
            self.ignore = ignore.split(",")
        else:
            self.ignore = []

    def scan_folder_recursive(self, path: Path) -> ParseResult:
        source_files: Set[Path] = set()
        import_links: Dict[Module, Set[Module]] = {}

        for root, folders, files in os.walk(path):
            if "node_modules" in folders:
                folders.remove("node_modules")

            for source_file in files:
                if source_file.endswith(".py"):
                    full_path = Path(os.path.join(root, source_file))
                    self.logger.info("source_file_found", path=full_path)
                    source_module = Module.from_path(path, full_path)
                    self.known_local_modules.add(source_module)
                    source_files.add(full_path)
        self.logger.debug("list_source_modules", source_modules=self.known_local_modules)

        for source_file in source_files:
            source_module = Module.from_path(path, source_file)
            file_links = self._handle_file(path, source_file)
            self.logger.debug("module_links", module=source_module, links=file_links)
            import_links[source_module] = file_links

        return ParseResult(source_modules=self.known_local_modules, import_links=import_links)

    def _handle_file(self, root: Path, path: Path) -> Set[Module]:
        source_module = Module.from_path(root, path)
        file_contents = self._parse_source_file(path)
        import_declarations = self._scan_imports(path, file_contents)
        self.logger.debug("imports_scanned", path=path, module=source_module, declarations=import_declarations)

        modules = set()
        for decl in import_declarations:
            modules.update(self._convert_import_declarations_to_modules(source_module, decl))
        return modules

    def _parse_source_file(self, path: Path) -> str:
        with open(path, mode="r", encoding="utf-8") as hndl:
            return hndl.read()

    def _scan_imports(self, path: Path, contents: str) -> Set[ImportDeclaration]:
        tree = ast.parse(contents, str(path))
        visitor = ImportNodeVisitor()
        visitor.visit(tree)
        return visitor.declarations

    def _parse_import_declaration(self, match: Match[str]) -> ImportDeclaration:
        groups = match.groupdict()
        source = None
        modules = None

        if "source" in groups:
            source = groups["source"].strip()
        if "modules" in groups:
            modules = frozenset(x.strip() for x in groups["modules"].split(","))

        return ImportDeclaration(source, modules)

    def _resolve_module(self, source_module: Module, target_module_name: str) -> Module:
        # Try a child module first
        decl_module = source_module.join(target_module_name)
        if decl_module in self.known_local_modules:
            return decl_module
        # Try a sibling module
        parent_module = source_module.parent()
        if parent_module:
            decl_module = parent_module.join(target_module_name)
            if decl_module in self.known_local_modules:
                return decl_module
        # It must be an external module/stdlib module
        return Module(name=target_module_name)

    def _convert_import_declarations_to_modules(
        self, source_module: Module, declaration: ImportDeclaration
    ) -> Set[Module]:
        modules = set()
        if declaration.source is not None:
            # That's a single import
            decl_module = self._resolve_module(source_module, declaration.source)
            if decl_module == source_module:
                return modules
            modules.add(decl_module)
        else:
            # It can be multiple imports
            for module in declaration.modules:
                decl_module = self._resolve_module(source_module, module)
                if decl_module == source_module:
                    continue
        return modules
