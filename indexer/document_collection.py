import os
from pathlib import Path
from dataclasses import dataclass, field

@dataclass(order = True, frozen = True)
class Document:
    id: int
    path: Path = field(compare = False)

@dataclass
class DocumentCollection:
    directory: Path

    def __iter__(self):
        entries = os.scandir(self.directory)
        txtFilter = lambda e: e.name.endswith(".txt")
        filteredEntries = filter(txtFilter, entries)
        sortedEntries = sorted(filteredEntries, key = lambda e: e.name)
        for i, directoryEntry in enumerate(sortedEntries):
            if not directoryEntry.is_file(): continue
            yield Document(i, Path(directoryEntry.path))
