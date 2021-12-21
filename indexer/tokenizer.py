import typing
from io import StringIO
from . scanner import Scanner
from . stop_list import StopList
from . normalizer import Normalizer
from dataclasses import dataclass, field

@dataclass
class Tokenizer:
    scanner: Scanner
    stopList: StopList
    normalizer: Normalizer
    text: typing.TextIO = field(default_factory = lambda: StringIO())

    def __call__(self, text):
        self.text = text
        return self

    def __iter__(self):
        for token in self.scanner(self.text):
            term = self.normalizer(token)
            if self.stopList is not None and term in self.stopList: continue
            yield term
