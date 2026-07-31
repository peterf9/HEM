from dataclasses import dataclass, field
from typing import List

from hem.contracts.asset import Asset
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.statistics import BuildStatistics


@dataclass
class BuildContext:
    assets: List[Asset] = field(default_factory=list)
    statistics: BuildStatistics = field(default_factory=BuildStatistics)
    manifest: BuildManifest = field(default_factory=BuildManifest)
