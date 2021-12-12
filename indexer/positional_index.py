import pickle
from io import StringIO
from . tokenizer import Tokenizer
from collections import OrderedDict
from dataclasses import dataclass, field
from . document_collection import DocumentCollection, Document

@dataclass
class Token:
    term: str
    position: int
    document: Document

@dataclass
class Posting:
    documentID: int
    frequency: int
    positions: list[int]

@dataclass
class PostingsList:
    term: str
    frequency: int = 0
    postings: list[Posting] = field(default_factory = lambda: [])

    def update(self, token):
        raise NotImplementedError

@dataclass
class PositionalIndex:
    tokenizer: Tokenizer = field(repr = False)
    documentCollection: DocumentCollection  = field(repr = False)
    dictionary: OrderedDict[str, PostingsList]

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeDictionary()

    def computeDictionary(self):
        self.dictionary = OrderedDict()
        for document in self.documentCollection:
            self.indexDocument(document)

    def indexDocument(self, document):
        with open(document.path) as file:
            for i, term in enumerate(self.tokenizer(file)):
                self.indexToken(Token(term, i, document))

    def indexToken(self, token):
        postingsList = self.dictionary.get(token.term)
        if not postingsList: postingsList = PostingsList(token.term)
        self.dictionary[token.term] = postingsList
        postingsList.update(token)

    #######
    # Query
    #######

    def phraseQuery(self, phrase):
        tokens = self.tokenizer(StringIO(phrase))
        postingsLists = [self.dictionary[token] for token in tokens]
        raise NotImplementedError

    ###########
    # Load/Save
    ###########

    def save(self):
        with open(self.documentCollection.directory / ".index", "wb") as file:
            # Avoid pickling the runtime text fields.
            del self.tokenizer.text
            del self.tokenizer.scanner.text

            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, directory):
        with open(directory / ".index", "rb") as file:
            return pickle.load(file)
