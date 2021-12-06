from io import StringIO
from tokenizer import Tokenizer
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
    tokenizer: Tokenizer
    dictionary: dict[str, PostingsList]

    def phraseQuery(self, phrase):
        for i, token in enumerate(self.tokenizer(StringIO(phrase))):
            raise NotImplementedError
