from dataclasses import dataclass, field
from typing import Dict, List, Set

from hem.contracts.asset import Asset


@dataclass
class BuildStatistics:
    total_assets: int = 0
    total_providers: int = 0
    total_files_generated: int = 0
    providers_used: Set[str] = field(default_factory=set)

    def record_assets(self, assets: List[Asset]) -> None:
        self.total_assets = len(assets)
        self.providers_used = {a.provider for a in assets if a.provider}
        self.total_providers = len(self.providers_used)
