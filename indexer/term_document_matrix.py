import numpy
import pickle
from math import log10
from . tokenizer import Tokenizer
from dataclasses import dataclass
from collections import OrderedDict
from scipy.sparse import spmatrix, lil_matrix
from . document_collection import DocumentCollection

@dataclass
class TermInfo:
    index: int
    inverseDocumentFrequency: float

@dataclass
class TermDocumentMatrix:
    tokenizer: Tokenizer
    documentCollection: DocumentCollection
    matrix: spmatrix
    termInfos: OrderedDict[str, TermInfo]

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection, positionalIndex):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeMatrix(positionalIndex)

    def computeMatrix(self, positionalIndex):
        self.termInfos = OrderedDict()
        numberOfTerms = len(positionalIndex.dictionary)
        numberOfDocuments = positionalIndex.numberOfDocuments
        matrix = lil_matrix((numberOfTerms, numberOfDocuments))
        postingsListsEnumerator = enumerate(positionalIndex.dictionary.items())
        for termIndex, (term, postingsList) in postingsListsEnumerator:
            documentFrequency = len(postingsList.postings)
            inverseDocumentFrequency = log10(numberOfDocuments / documentFrequency)
            self.termInfos[term] = TermInfo(termIndex, inverseDocumentFrequency)
            for posting in postingsList.postings:
                termFrequency = posting.frequency
                weight = termFrequency * inverseDocumentFrequency
                matrix[termIndex, posting.document.id] = weight
        matrix = matrix.tocsc()

        columnsLengths = numpy.sqrt(matrix.multiply(matrix).sum(axis = 0).A1)
        columnsLengthsReciprocal = numpy.reciprocal(columnsLengths,
            out = numpy.zeros_like(columnsLengths), where = columnsLengths != 0)
        self.matrix = matrix.multiply(columnsLengthsReciprocal)

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

    ######
    # Dump
    ######

    def dump(self):
        terms = list(self.termInfos.keys())
        for document in self.documentCollection:
            documentPath = repr(document.path.as_posix())
            print(f"Document: {documentPath}")
            documentColumn = self.matrix.getcol(document.id).tocoo()
            for i, value in zip(documentColumn.row, documentColumn.data):
                print(f"  {terms[i]} : {value}")
