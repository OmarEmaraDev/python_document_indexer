from indexer.normalizer import LowerCaseNormalizer

class TestLowerCaseNormalizer:
    def test_Name(self):
        normalizer = LowerCaseNormalizer()
        assert normalizer("Bob") == "bob"
