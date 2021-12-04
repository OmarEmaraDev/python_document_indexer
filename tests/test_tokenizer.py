from io import StringIO
from indexer.tokenizer import WhiteSpaceTokenizer

class TestWhiteSpaceTokenizer:
    def test_Spaces(self):
        tokenizer = WhiteSpaceTokenizer(StringIO("Word Word"))
        assert list(tokenizer) == ["Word", "Word"]

    def test_Tabs(self):
        tokenizer = WhiteSpaceTokenizer(StringIO("Word \t Word"))
        assert list(tokenizer) == ["Word", "Word"]

    def test_NewLines(self):
        tokenizer = WhiteSpaceTokenizer(StringIO("\nWord \n\n Word\n"))
        assert list(tokenizer) == ["Word", "Word"]

    def test_Apostrophe(self):
        tokenizer = WhiteSpaceTokenizer(StringIO("Isn't Word"))
        assert list(tokenizer) == ["Isn't", "Word"]

    def test_Parenthesis(self):
        tokenizer = WhiteSpaceTokenizer(StringIO("Word (Word) Word"))
        assert list(tokenizer) == ["Word", "Word", "Word"]
