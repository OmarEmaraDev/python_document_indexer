from abc import ABC, abstractmethod

class StopList(ABC):
    @abstractmethod
    def __contains__(self, word: str) -> bool:
        raise NotImplementedError

class ReutersRCV1StopList(StopList):
    stopList = set(("a", "an", "and", "are", "as", "at", "be", "by", "for",
                   "from", "has", "he", "in", "is", "it", "its", "of", "on",
                   "that", "the", "to", "was", "were", "will", "with"))
    def __contains__(self, word):
        return word in self.stopList
