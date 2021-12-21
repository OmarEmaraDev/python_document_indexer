# Python Document Indexer

A minimal document indexer written in Python. Computes a positional index for a
document collection and a term document matrix, then allows a ranked query
based on the index and the matrix. A college assignment.

# Dependencies

- Numpy.
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
    query     Query the documents that includes the input phrase. And sort based on cosine similarity.
    dump      Dump the positional index for collection.
```

Index:

```
usage: python -m indexer index [-h] [--no-stop-words] [COLLECTION]

Compute the index and term document matrix for collection.

positional arguments:
  COLLECTION           The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help           show this help message and exit
  --no-stop-words, -n  Do not remove stop words.
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

Dump:

```
usage: python -m indexer dump [-h] {index,matrix} [COLLECTION]

Dump the positional index for collection.

positional arguments:
  {index,matrix}  Which structure to dump.
  COLLECTION      The path to the directory containing the document collection. Defaults to the curent working directory.

options:
  -h, --help      show this help message and exit
```

# Test

This project uses `pytest` for unit testing. Run the tests as follows:

```
pytest
```
