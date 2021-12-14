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

def printErrorAndExit(error, exitCode = 1):
    print("indexer: " + error)
    sys.exit(exitCode)

def index(arguments):
    scanner = WhiteSpaceScanner()
    stopList = ReutersRCV1StopList()
    normalizer = LowerCaseNormalizer()
    tokenizer = Tokenizer(scanner, stopList, normalizer)
    documentCollection = DocumentCollection(arguments.collection)
    positionalIndex = PositionalIndex(tokenizer, documentCollection)
    positionalIndex.save()

def query(arguments):
    pass

def validateDump(arguments):
    if not (arguments.collection / ".index").exists():
        printErrorAndExit("No index exists. Run 'indexer index' first!")

def dump(arguments):
    validateDump(arguments)
    positionalIndex = PositionalIndex.load(arguments.collection)
    positionalIndex.dump()

def parseArguments():
    parser = ArgumentParser(prog = "indexer")
    subParsers = parser.add_subparsers(title = "Actions", required = True,
        description = "The action to apply over the input document collection.",
        metavar = "ACTION")

    collectionHelp = "The path of the directory containing the document collection."

    indexHelp = "Compute the index for collection."
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

