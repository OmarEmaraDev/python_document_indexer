from abc import ABC, abstractmethod

class StopList(ABC):
    @abstractmethod
    def __contains__(self, word: str) -> bool:
        raise NotImplementedError

class ReutersRCV1StopList(StopList):
    def __contains__(self, word):
        raise NotImplementedError
