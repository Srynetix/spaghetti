from spaghetti.parser.import_declaration import ImportDeclaration


class TestImportDeclaration:
    def test_hash(self):
        decl = ImportDeclaration(source=None, modules=frozenset())
        hash(decl)

    def test_str_no_source(self):
        assert str(ImportDeclaration(source=None, modules=frozenset("a"))) == "import {'a'}"

    def test_str_with_source(self):
        assert str(ImportDeclaration(source="b", modules=frozenset("a"))) == "from b import {'a'}"

    def test_repr(self):
        decl = ImportDeclaration(source=None, modules=frozenset("a"))
        assert str(decl) == repr(decl)
