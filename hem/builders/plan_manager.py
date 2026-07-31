from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from hem.builders.build_manager import BuildManager
from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths


@dataclass
class PlanDiff:
    new_assets: List[str] = field(default_factory=list)
    new_entities: List[str] = field(default_factory=list)
    new_files: List[Path] = field(default_factory=list)


class PlanManager:

    def plan(self) -> PlanDiff:
        manager = BuildManager()
        context = manager.build()

        diff = PlanDiff(
            new_assets=[a.id for a in context.assets],
            new_entities=[e.entity_id for e in (context.manifest.generated_entities if context.manifest else [])],
            new_files=context.manifest.generated_files if context.manifest else [],
        )

        return diff
