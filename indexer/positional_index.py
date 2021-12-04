from io import StringIO
from stop_list import StopList
from tokenizer import Tokenizer
from normalizer import Normalizer
from dataclasses import dataclass, field

@dataclass
class Posting:
    documentID: int
    frequency: int
    positions: list[int]

@dataclass
class PostingsList:
    term: str
    frequency: int = 0
    postings: dict[Posting] = field(default_factory = lambda: [])

@dataclass
class PositionalIndex:
    stop_list: StopList
    tokenizer: Tokenizer
    normalizer: Normalizer
    dictionary: dict[str, PostingsList]

    def phraseQuery(self, phrase):
        for i, token in enumerate(self.tokenizer(StringIO(phrase))):
            term = self.normalizer(token)
            if term in self.stop_list: continue

            raise NotImplementedError
