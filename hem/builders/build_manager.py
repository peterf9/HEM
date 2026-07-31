from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from hem.generators.provider import ProviderGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.paths import Paths
from hem.validators.asset_validator import AssetValidator


@dataclass
class BuildReport:
    asset_count: int = 0
    provider_count: int = 0
    template_count: int = 0
    generated_files: List[Path] = field(default_factory=list)


class BuildManager:
    def __init__(self):
        self.loader = AssetLoader(Paths.assets())
        self.validator = AssetValidator()

    def build(self) -> BuildReport:
        assets = self.loader.load()
        self.validator.validate(assets)

        report = BuildReport(
            asset_count=len(assets),
            provider_count=len(set(a.provider for a in assets if a.provider)),
            template_count=len(assets),
        )

        provider_output = Paths.hem_package_output() / "templates" / "provider.yaml"
        provider_gen = ProviderGenerator(Paths.templates())
        provider_gen.generate(assets, provider_output)

        report.generated_files.append(provider_output)

        return report
