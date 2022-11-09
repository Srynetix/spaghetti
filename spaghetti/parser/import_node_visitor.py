import ast
from typing import Any, Set

from .import_declaration import ImportDeclaration


class ImportNodeVisitor(ast.NodeVisitor):
    declarations: Set[ImportDeclaration]

    def __init__(self):
        self.declarations = set()

    def visit_Import(self, node: ast.Import) -> Any:
        declaration = ImportDeclaration(
            source=None, modules=frozenset(name.name for name in node.names)
        )
        self.declarations.add(declaration)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        declaration = ImportDeclaration(
            source=node.module, modules=frozenset(name.name for name in node.names)
        )
        self.declarations.add(declaration)
