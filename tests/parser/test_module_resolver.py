from spaghetti.models.module import Module
from spaghetti.parser.import_declaration import ImportDeclaration
from spaghetti.parser.module_resolver import ModuleResolver


class TestModuleResolver:
    def test_convert_import_declaration(self) -> None:
        known_local_modules = {
            Module("module"),
            Module("module.a"),
            Module("module.b"),
            Module("module.c"),
        }
        resolver = ModuleResolver(known_local_modules)

        assert resolver.convert_import_declaration_to_modules(
            Module("module.a"), ImportDeclaration(source="module", modules=frozenset({"b"}))
        ) == {Module("module"), Module("module.b")}

    def test_sibling_resolver(self) -> None:
        known_local_modules = {
            Module("module"),
            Module("module.a"),
            Module("module.a.one"),
            Module("module.a.two"),
        }
        resolver = ModuleResolver(known_local_modules)
        import_decl = ImportDeclaration(source=None, modules=frozenset({"two"}))

        assert resolver.convert_import_declaration_to_modules(
            Module("module.a.one"), import_decl
        ) == {Module("module.a.two")}
