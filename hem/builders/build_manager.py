from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from hem.generators.provider import ProviderGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.build_context import BuildContext
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
        context = BuildContext()
        context.assets = self.loader.load()
        self.validator.validate(context.assets)
        context.statistics.record_assets(context.assets)

        provider_output = Paths.hem_package_output() / "templates.yaml"
        provider_gen = ProviderGenerator(Paths.templates())
        provider_gen.generate(context.assets, provider_output)

        context.manifest.add_file(provider_output)
        context.statistics.total_files_generated = len(context.manifest.generated_files)

        report = BuildReport(
            asset_count=context.statistics.total_assets,
            provider_count=context.statistics.total_providers,
            template_count=context.statistics.total_assets,
            generated_files=context.manifest.generated_files,
        )

        return report
