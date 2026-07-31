from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class GeneratedEntity:
    entity_id: str
    platform: str
    generator: str


@dataclass
class BuildManifest:
    hem_version: str
    started_at: datetime
    manifest_version: int = 1
    finished_at: datetime | None = None
    generated_files: list[Path] = field(default_factory=list)
    generated_entities: list[GeneratedEntity] = field(default_factory=list)
