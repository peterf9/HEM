from dataclasses import dataclass, field
from pathlib import Path

from hem.contracts.asset import Asset
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.statistics import BuildStatistics


@dataclass
class BuildContext:
    assets: list[Asset] = field(default_factory=list)
    statistics: BuildStatistics = field(default_factory=BuildStatistics)
    manifest: BuildManifest | None = None
    output_dir: Path | None = None
    version: str = "0.1.0"
