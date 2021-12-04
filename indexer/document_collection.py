import os
from dataclasses import dataclass

@dataclass
class Document:
    identifier: int
    path: str

@dataclass
class DocumentCollection:
    directory: str

    def __iter__(self):
        for i, directoryEntry in enumerate(os.scandir(self.directory)):
            if not directoryEntry.is_file(): continue
            yield Document(i, directoryEntry.path)
