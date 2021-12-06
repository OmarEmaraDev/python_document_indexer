from tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix

@dataclass
class TermDocumentMatrix:
    tokenizer: Tokenizer
    matrix: spmatrix

    def computeSimilarity(self, phrase, document):
        raise NotImplementedError
