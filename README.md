# Python Document Indexer

A minimal document indexer written in Python. A college assignment.

# Dependencies

- Scipy.

# Run

General:

```
usage: python -m indexer [-h] ACTION ...

options:
  -h, --help  show this help message and exit

Actions:
  The action to apply over the input document collection.

  ACTION
    index     Compute the index and term document matrix for collection.
    query     Query the documents that includes the input phrase.
    rank      Rank the documents according to similarity to the input phrase.
    dump      Dump the positional index for collection.
```

Index:

```
usage: python -m indexer index [-h] [COLLECTION]

Compute the index and term document matrix for collection.

positional arguments:
  COLLECTION  The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help  show this help message and exit
```

Query:

```
usage: python -m indexer query [-h] PHRASE [COLLECTION]

Query the documents that includes the input phrase.

positional arguments:
  PHRASE      The phrase to query for.
  COLLECTION  The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help  show this help message and exit
```

Rank:

```
usage: python -m indexer rank [-h] PHRASE [COLLECTION]

Rank the documents according to similarity to the input phrase.

positional arguments:
  PHRASE      The phrase to rank documents against.
  COLLECTION  The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help  show this help message and exit
```

Dump:

```
usage: python -m indexer dump [-h] [COLLECTION]

Dump the positional index for collection.

positional arguments:
  COLLECTION  The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help  show this help message and exit
```

# Test

This project uses `pytest` for unit testing. Run the tests as follows:

```
pytest
```
