import os
import sys
from pathlib import Path
from . tokenizer import Tokenizer
from argparse import ArgumentParser
from . scanner import WhiteSpaceScanner
from . stop_list import ReutersRCV1StopList
from . normalizer import LowerCaseNormalizer
from . positional_index import PositionalIndex
from . document_collection import DocumentCollection
from . term_document_matrix import TermDocumentMatrix

PROGRAM_NAME = "python -m indexer"
INDEX_NAME = ".index"
MATRIX_NAME = ".matrix"

def printErrorAndExit(error, exitCode = 1):
    print(PROGRAM_NAME + ": " + error)
    sys.exit(exitCode)

def index(arguments):
    scanner = WhiteSpaceScanner()
    stopList = ReutersRCV1StopList()
    normalizer = LowerCaseNormalizer()
    tokenizer = Tokenizer(scanner, stopList, normalizer)
    documentCollection = DocumentCollection(arguments.collection)

    positionalIndex = PositionalIndex(tokenizer, documentCollection)
    positionalIndex.save(INDEX_NAME)

    termDocumentMatrix = TermDocumentMatrix(
        tokenizer, documentCollection, positionalIndex)
    termDocumentMatrix.save(MATRIX_NAME)

def query(arguments):
    positionalIndex = PositionalIndex.load(arguments.collection / INDEX_NAME)
    for match in positionalIndex.phraseQuery(arguments.phrase):
        print(match)

def rank(arguments):
    pass

def validateDump(arguments):
    if not (arguments.collection / INDEX_NAME).exists():
        printErrorAndExit("No index exists."
            f" Run '{PROGRAM_NAME} index {str(arguments.collection)}' first!")

def dump(arguments):
    validateDump(arguments)
    positionalIndex = PositionalIndex.load(arguments.collection / INDEX_NAME)
    positionalIndex.dump()

def parseArguments():
    parser = ArgumentParser(prog = PROGRAM_NAME)
    subParsers = parser.add_subparsers(title = "Actions", required = True,
        description = "The action to apply over the input document collection.",
        metavar = "ACTION")

    collectionHelp = (
        "The path to the directory containing the document collection."
        " Defaults to the curent working directory."
    )

    indexHelp = "Compute the index and term document matrix for collection."
    indexParser = subParsers.add_parser("index",
        help = indexHelp, description = indexHelp)
    indexParser.add_argument("collection", type = Path, nargs = "?",
        metavar = "COLLECTION", default = Path.cwd(), help = collectionHelp)
    indexParser.set_defaults(handler = index)

    queryHelp = "Query the documents that includes the input phrase."
    queryParser = subParsers.add_parser("query",
        help = queryHelp, description = queryHelp)
    queryParser.add_argument("phrase", metavar = "PHRASE",
        help = "The phrase to query for.")
    queryParser.add_argument("collection", type = Path, nargs = "?",
        metavar = "COLLECTION", default = Path.cwd(), help = collectionHelp)
    queryParser.set_defaults(handler = query)

    rankHelp = "Rank the documents according to similarity to the input phrase."
    rankParser = subParsers.add_parser("rank",
        help = rankHelp, description = rankHelp)
    rankParser.add_argument("phrase", metavar = "PHRASE",
        help = "The phrase to rank documents against.")
    rankParser.add_argument("collection", type = Path, nargs = "?",
        metavar = "COLLECTION", default = Path.cwd(), help = collectionHelp)
    rankParser.set_defaults(handler = rank)

    dumpHelp = "Dump the positional index for collection."
    dumpParser = subParsers.add_parser("dump",
        help = dumpHelp, description = dumpHelp)
    dumpParser.add_argument("collection", type = Path, nargs = "?",
        metavar = "COLLECTION", default = Path.cwd(), help = collectionHelp)
    dumpParser.set_defaults(handler = dump)

    return parser.parse_args()

def validateCommonArguments(arguments):
    if not arguments.collection.is_dir():
        printErrorAndExit("Collection should be a path to a directory.")

def main():
    arguments = parseArguments()
    validateCommonArguments(arguments)
    arguments.handler(arguments)

if __name__ == "__main__":
    sys.exit(main())

