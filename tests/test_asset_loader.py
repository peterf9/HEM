from hem.loaders.asset_loader import AssetLoader
from hem.runtime.paths import Paths


def test_load_assets():

    loader = AssetLoader(Paths.assets())

    assets = loader.load()

    assert len(assets) > 0
