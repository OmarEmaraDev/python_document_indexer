from stop_list import StopList
from tokenizer import Tokenizer
from normalizer import Normalizer
from dataclasses import dataclass
from document_collection import DocumentCollection
from positional_index import PositionalIndex, PostingsList, Posting

@dataclass
class Indexer:
    stopList: StopList
    tokenizer: Tokenizer
    normalizer: Normalizer
    documentCollection: DocumentCollection

    ##################
    # Positional Index
    ##################

    def computeIndex(self):
        index = self.createEmptyIndex()
        for document in self.documentCollection:
            self.indexDocument(index, document)

    def createEmptyIndex(self):
        return PositionalIndex(self.stopList, self.tokenizer, self.normalizer, dict())

    def indexDocument(self, index, document):
        with open(document.path) as file:
            for i, token in enumerate(self.tokenizer(file)):
                self.indexToken(index, document, token, i)

    def indexToken(self, index, document, token, position):
        term = self.normalizer(token)
        if term in self.stopList: return
        postingsList = index.dictionary.get(term)
        if not postingsList: PostingsList(term)
        index.dictionary[term] = postingsList
        self.updatePostingsList(document, postingsList)

    def updatePostingsList(self, document, postingsList):
        raise NotImplementedError

    ######################
    # Term Document Matrix
    ######################

    def computeTermDocumentMatrix(self):
        raise NotImplementedError
