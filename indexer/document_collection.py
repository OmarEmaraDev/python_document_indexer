import os
from pathlib import Path
from dataclasses import dataclass, field

@dataclass(order = True)
class Document:
    id: int
    path: Path = field(compare = False)

@dataclass
class DocumentCollection:
    directory: Path

    def __iter__(self):
        for i, directoryEntry in enumerate(os.scandir(self.directory)):
            if not directoryEntry.is_file(): continue
            if directoryEntry.name == ".index": continue
            yield Document(i, Path(directoryEntry.path))
