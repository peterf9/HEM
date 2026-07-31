from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from hem.contracts.asset import Asset
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.execution_context import ExecutionContext
from hem.runtime.statistics import BuildStatistics


@dataclass
class BuildContext(ExecutionContext):
    assets: List[Asset] = field(default_factory=list)
    inventory: List[Asset] = field(default_factory=list)
    statistics: BuildStatistics = field(default_factory=BuildStatistics)
    manifest: Optional[BuildManifest] = None
