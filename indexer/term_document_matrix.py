from stop_list import StopList
from tokenizer import Tokenizer
from scipy.sparse import spmatrix
from normalizer import Normalizer
from dataclasses import dataclass

@dataclass
class TermDocumentMatrix:
    stopList: StopList
    tokenizer: Tokenizer
    normalizer: Normalizer
    matrix: spmatrix

    def computeSimilarity(self, phrase, document):
        raise NotImplementedError
