import typing
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Normalizer(ABC):
    @abstractmethod
    def __call__(self, term: str) -> str:
        raise NotImplementedError

class LowerCaseNormalizer(Normalizer):
    def __call__(self, token):
        return token.lower()
