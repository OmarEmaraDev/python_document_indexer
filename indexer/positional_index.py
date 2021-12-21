import pickle
from io import StringIO
from . tokenizer import Tokenizer
from collections import OrderedDict
from dataclasses import dataclass, field
from . document_collection import DocumentCollection, Document

@dataclass(frozen = True)
class Match:
    position: int
    document: Document

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

    def forwardIntersect(self, targetPosting, proximity):
        answer = set()
        positionIndex = 0
        targetPositionIndex = 0
        positions = self.positions
        targetPositions = targetPosting.positions
        while positionIndex != len(positions) and targetPositionIndex != len(targetPositions):
            position = positions[positionIndex]
            targetPosition = targetPositions[targetPositionIndex]
            if targetPosition - position == proximity:
                answer.add(Match(position, self.document))
                positionIndex += 1
                targetPositionIndex += 1
            elif targetPosition - position > proximity:
                positionIndex += 1
            else:
                targetPositionIndex += 1
        return answer

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

    def forwardIntersect(self, targetPostingsList, proximity):
        answer = set()
        postingIndex = 0
        targetPostingIndex = 0
        postings = self.postings
        targetPostings = targetPostingsList.postings
        while postingIndex != len(postings) and targetPostingIndex != len(targetPostings):
            posting = postings[postingIndex]
            targetPosting = targetPostings[targetPostingIndex]
            if posting.document.id == targetPosting.document.id:
                answer |= posting.forwardIntersect(targetPosting, proximity)
                postingIndex += 1
                targetPostingIndex += 1
            elif posting.document.id > targetPosting.document.id:
                targetPostingIndex += 1
            else:
                postingIndex += 1
        return answer

    def getMatchesForAll(self):
        result = set()
        for posting in self.postings:
            for position in posting.positions:
                result.add(Match(position, posting.document))
        return result

    def dump(self, indentation = 0):
        print(" " * indentation, end = "")
        print(f"Term: {repr(self.term)}, Frequency: {self.frequency}")
        for posting in self.postings:
            posting.dump(indentation + 2)


@dataclass
class PositionalIndex:
    tokenizer: Tokenizer
    numberOfDocuments: int
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
        self.sortDictionary()

    def computeDictionary(self):
        self.numberOfDocuments = 0
        self.dictionary = OrderedDict()
        for document in self.documentCollection:
            self.numberOfDocuments += 1
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

    def sortDictionary(self):
        self.dictionary = OrderedDict(sorted(self.dictionary.items()))

    #######
    # Query
    #######

    def phraseQuery(self, phrase):
        terms = self.tokenizer(StringIO(phrase))
        postingsLists = [self.dictionary[term] for term in terms]
        if len(postingsLists) == 0: return set()
        firstPostingsList = postingsLists[0]
        if len(postingsLists) == 1: return firstPostingsList.getMatchesForAll()

        matches = []
        for i, postingsList in enumerate(postingsLists[1:], 1):
            matches.append(firstPostingsList.forwardIntersect(postingsList, i))
        return set.intersection(*matches)

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
