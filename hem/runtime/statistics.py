from dataclasses import dataclass, field
from typing import Set


@dataclass
class BuildStatistics:
    assets_loaded: int = 0
    assets_validated: int = 0
    entities_generated: int = 0
    files_generated: int = 0
    warnings: int = 0
    errors: int = 0
    build_time_ms: float = 0.0
    providers_used: Set[str] = field(default_factory=set)
