from pathlib import Path
from typing import List

import yaml

from hem.contracts.asset import Asset


class AssetLoader:
    """
    Loads Asset definitions from src/assets.
    """

    def __init__(self, assets_path: Path):
        self.assets_path = assets_path

    def load(self) -> List[Asset]:
        assets: List[Asset] = []

        if not self.assets_path.exists():
            return assets

        for file in sorted(self.assets_path.glob("*.yaml")):
            with file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            asset = Asset.model_validate(data["asset"])
            assets.append(asset)

        return assets
