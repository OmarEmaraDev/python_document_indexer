import typing
from io import StringIO
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class Scanner(ABC):
    text: typing.TextIO = field(default_factory = lambda: StringIO())

    def __call__(self, text):
        self.text = text
        return self

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

class WhiteSpaceScanner(Scanner):
    def __iter__(self):
        raise NotImplementedError
