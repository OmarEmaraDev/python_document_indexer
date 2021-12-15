from io import StringIO
from indexer.tokenizer import Tokenizer
from indexer.scanner import WhiteSpaceScanner
from indexer.stop_list import ReutersRCV1StopList
from indexer.normalizer import LowerCaseNormalizer

scanner = WhiteSpaceScanner()
stopList = ReutersRCV1StopList()
normalizer = LowerCaseNormalizer()
tokenizer = Tokenizer(scanner, stopList, normalizer)

class TestWhiteSpaceScanner:
    def test_NoStopWords(self):
        tokenizer(StringIO("Word Word"))
        assert list(tokenizer) == ["word", "word"]

    def test_StopWords(self):
        tokenizer(StringIO("As Word To\t Word"))
        assert list(tokenizer) == ["word", "word"]
