from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from hem.contracts.asset import Asset
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.paths import Paths
from hem.runtime.statistics import BuildStatistics


@dataclass
class ExecutionContext:
    version: str = "0.1.0"
    project_root: Path = field(default_factory=Paths.project_root)
    output_dir: Path = field(default_factory=Paths.hem_package_output)
    metadata: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None
