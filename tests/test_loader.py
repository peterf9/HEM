from pathlib import Path
from hem.loaders.asset_loader import AssetLoader


def test_asset_loader():
    loader = AssetLoader(Path("src/assets"))
    assets = loader.load()
    assert len(assets) > 0
    assert any(a.id == "brume" for a in assets)
