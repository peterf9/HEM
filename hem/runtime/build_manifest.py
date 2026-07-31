from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class BuildManifest:
    generated_files: List[Path] = field(default_factory=list)

    def add_file(self, path: Path) -> None:
        if path not in self.generated_files:
            self.generated_files.append(path)
