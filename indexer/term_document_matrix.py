import pickle
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

    def __init__(self, tokenizer, documentCollection, positionalIndex):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeMatrix(positionalIndex)

    def computeMatrix(self, positionalIndex):
        pass

    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        pass

    ###########
    # Load/Save
    ###########

    def save(self, fileName):
        with open(self.documentCollection.directory / fileName, "wb") as file:
            # Avoid pickling the runtime text fields.
            if hasattr(self.tokenizer, "text"): del self.tokenizer.text
            if hasattr(self.tokenizer.scanner, "text"): del self.tokenizer.scanner.text

            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)
