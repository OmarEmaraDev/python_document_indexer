from indexer.stop_list import ReutersRCV1StopList

class TestReutersRCV1StopList:
    stopList = ("a", "an", "and", "are", "as", "at", "be", "by", "for",
                "from", "has", "he", "in", "is", "it", "its", "of", "on",
                "that", "the", "to", "was", "were", "will", "with")

    def test_StopWord(self):
        for stopWord in self.stopList:
            assert stopWord in ReutersRCV1StopList()

    def test_NonStopWord(self):
        assert "Test" not in ReutersRCV1StopList()
