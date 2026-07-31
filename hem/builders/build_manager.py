import time
from datetime import datetime

from hem.generators.manifest import ManifestGenerator
from hem.generators.provider import ProviderGenerator
from hem.generators.report import ReportGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.paths import Paths
from hem.validators.asset_validator import AssetValidator


class BuildManager:

    def build(self) -> BuildContext:
        start_time = time.perf_counter()
        started_at = datetime.now()

        context = BuildContext()
        context.manifest = BuildManifest(
            hem_version=context.version,
            started_at=started_at,
        )

        context.assets = AssetLoader(Paths.assets()).load()
        context.statistics.assets_loaded = len(context.assets)

        AssetValidator().validate(context.assets)
        context.statistics.assets_validated = len(context.assets)

        ProviderGenerator(Paths.templates()).generate(context)

        end_time = time.perf_counter()
        context.manifest.finished_at = datetime.now()
        context.statistics.build_time_ms = (end_time - start_time) * 1000

        ManifestGenerator(Paths.templates()).generate(context)
        ReportGenerator().generate(context)

        return context
