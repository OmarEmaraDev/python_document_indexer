import typing
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Tokenizer(ABC):
    text: typing.TextIO

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        raise NotImplementedError

class WhiteSpaceTokenizer(Tokenizer):
    def __next__(self):
        raise NotImplementedError
