from io import StringIO
from indexer.scanner import WhiteSpaceScanner

class TestWhiteSpaceScanner:
    def test_Spaces(self):
        scanner = WhiteSpaceScanner(StringIO("Word Word"))
        assert list(scanner) == ["Word", "Word"]

    def test_Tabs(self):
        scanner = WhiteSpaceScanner(StringIO("Word \t Word"))
        assert list(scanner) == ["Word", "Word"]

    def test_NewLines(self):
        scanner = WhiteSpaceScanner(StringIO("\nWord \n\n Word\n"))
        assert list(scanner) == ["Word", "Word"]

    def test_Apostrophe(self):
        scanner = WhiteSpaceScanner(StringIO("Isn't Word"))
        assert list(scanner) == ["Isn't", "Word"]

    def test_Parenthesis(self):
        scanner = WhiteSpaceScanner(StringIO("Word (Word) Word"))
        assert list(scanner) == ["Word", "Word", "Word"]
