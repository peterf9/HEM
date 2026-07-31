from hem.generators.provider import ProviderGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.paths import Paths


def test_provider_generator(tmp_path):
    loader = AssetLoader(Paths.assets())
    assets = loader.load()

    output_file = tmp_path / "templates.yaml"
    generator = ProviderGenerator(Paths.templates())
    generator.generate(assets, output_file)

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "HEM Brume Available" in content
    assert "unique_id: \"hem_brume_available\"" in content
