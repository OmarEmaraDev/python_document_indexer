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
        setOfDocs = list()
        answer = set()
        for i in range(len(postingsLists) - 1):
            plist = postingsLists[i: i+2]
            setOfDocs.append(set(self.positionalIntersect(plist[0], plist[1])))

        if setOfDocs != []:
            answer = set(setOfDocs[0])
            for s in setOfDocs:
                answer = answer & s
        return answer


    def positionalIntersect(self, posting1, posting2):
        answer = []

        list1 = iter(posting1.postings)
        list2 = iter(posting2.postings)

        for p1, p2 in zip(list1, list2):
            if p1.document.id == p2.document.id:
                l = []
                positions1 = iter(p1.positions)
                positions2 = iter(p2.positions)

                for pp1 in positions1:
                    for pp2 in positions2:
                        if abs(pp1 - pp2) <= 1:
                            l.append(pp2)
                        elif pp2 > pp1:
                            break
                        next(positions2, None)

                    while l != [] and abs(l[0] - pp1) > 1:
                        l.remove(l[0])
                    for ps in l:
                        answer.append(p1.document.id)
                    next(positions1, None)
                next(list1, None)
                next(list2, None)
            elif p1.document.id < p2.document.id:
                next(list1, None)
            else:
                next(list2, None)
        return answer


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
