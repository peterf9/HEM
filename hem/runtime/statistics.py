from dataclasses import dataclass


@dataclass
class BuildStatistics:
    assets_loaded: int = 0
    assets_validated: int = 0
    entities_generated: int = 0
    files_generated: int = 0
    warnings: int = 0
    errors: int = 0
    build_time_ms: float = 0.0
