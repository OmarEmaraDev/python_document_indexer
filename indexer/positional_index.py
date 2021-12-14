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

@dataclass(order = True)
class Posting:
    document: Document
    frequency: int = field(default = 0, compare = False)
    positions: list[int] = field(default_factory = lambda: [], compare = False)

    def update(self, token):
        self.frequency += 1
        self.positions.append(token.position)

    def dump(self, indentation = 0):
        print(" " * indentation, end = "")
        documentPath = repr(self.document.path.as_posix())
        print(f"Document: {documentPath}, Frequency: {self.frequency}")
        print(" " * (indentation + 2), end = "")
        print(self.positions)

@dataclass
class PostingsList:
    term: str
    frequency: int = 0
    postings: list[Posting] = field(default_factory = lambda: [])

    def update(self, token):
        self.frequency += 1
        posting = Posting(token.document)
        if posting in self.postings:
            posting = self.postings[self.postings.index(posting)]
        else:
            self.postings.append(posting)
        posting.update(token)

    def sort(self):
        self.postings.sort()

    def dump(self, indentation = 0):
        print(" " * indentation, end = "")
        print(f"Term: {repr(self.term)}, Frequency: {self.frequency}")
        for posting in self.postings:
            posting.dump(indentation + 2)


@dataclass
class PositionalIndex:
    tokenizer: Tokenizer
    documentCollection: DocumentCollection
    dictionary: OrderedDict[str, PostingsList]

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeDictionary()
        self.sortPostingsLists()

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

    def sortPostingsLists(self):
        for postingsList in self.dictionary.values():
            postingsList.sort()

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

    def save(self, fileName):
        with open(self.documentCollection.directory / fileName, "wb") as file:
            # Avoid pickling the runtime text fields.
            del self.tokenizer.text
            del self.tokenizer.scanner.text

            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)

    ######
    # Dump
    ######

    def dump(self):
        for postingsList in self.dictionary.values():
            postingsList.dump()
