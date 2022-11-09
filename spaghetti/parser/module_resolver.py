from typing import FrozenSet, Set

from structlog import get_logger

from spaghetti.models.module import Module

from .import_declaration import ImportDeclaration


class ModuleResolver:
    known_modules: Set[Module]

    def __init__(self, known_modules: Set[Module]) -> None:
        self.logger = get_logger("SourceParser")
        self.known_modules = known_modules

    def convert_import_declarations_to_modules(
        self, source_module: Module, declarations: Set[ImportDeclaration]
    ) -> Set[Module]:
        modules = set()
        for decl in declarations:
            modules.update(self.convert_import_declaration_to_modules(source_module, decl))
        return modules

    def convert_import_declaration_to_modules(
        self, source_module: Module, declaration: ImportDeclaration
    ) -> Set[Module]:
        modules = set()
        if declaration.source is not None:
            modules.update(
                self._convert_single_import_declaration_to_modules(
                    source_module, declaration.source, declaration.modules
                )
            )
        else:
            # It can be multiple imports
            for module in declaration.modules:
                decl_module = self._resolve_module(source_module, module)
                if decl_module == source_module:
                    continue
                modules.add(decl_module)
        return modules

    def _convert_single_import_declaration_to_modules(
        self, source_module: Module, decl_source: str, decl_modules: FrozenSet[str]
    ) -> Set[Module]:
        modules = set()

        decl_module = self._resolve_module(source_module, decl_source)
        if decl_module != source_module:
            self.logger.debug(
                "convert_single_import",
                source_module=source_module,
                decl_source=decl_source,
                module=decl_module,
            )
            modules.add(decl_module)

        for module in decl_modules:
            local_module = self._resolve_module(decl_module, module)
            if local_module != source_module and local_module in self.known_modules:
                self.logger.debug(
                    "convert_single_import",
                    source_module=source_module,
                    decl_source=decl_source,
                    module=local_module,
                    import_module=module,
                )
                modules.add(local_module)

        return modules

    def _resolve_module(self, source_module: Module, target_module_name: str) -> Module:
        # Try a child module first
        decl_module = source_module.join(target_module_name)
        if decl_module in self.known_modules:
            return decl_module

        # Try a sibling module
        parent_module = source_module.parent()
        if parent_module:
            decl_module = parent_module.join(target_module_name)
            if decl_module in self.known_modules:
                return decl_module

        # It must be an external module/stdlib module
        return Module(name=target_module_name)
