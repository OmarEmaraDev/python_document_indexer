import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Document:
    id: int
    path: Path

@dataclass
class DocumentCollection:
    directory: Path

    def __iter__(self):
        for i, directoryEntry in enumerate(os.scandir(self.directory)):
            if not directoryEntry.is_file(): continue
            if directoryEntry.name == ".index": continue
            yield Document(i, Path(directoryEntry.path))
