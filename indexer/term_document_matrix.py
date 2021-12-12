from . tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix
from . document_collection import DocumentCollection

@dataclass
class TermDocumentMatrix:
    tokenizer: Tokenizer
    documentCollection: DocumentCollection
    matrix: spmatrix

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeMatrix()

    def computeMatrix(self):
        raise NotImplementedError

    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        raise NotImplementedError
