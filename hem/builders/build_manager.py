import time
from datetime import datetime

from hem.events.event_bus import EventBus
from hem.generators.inventory import InventoryGenerator
from hem.generators.manifest import ManifestGenerator
from hem.generators.provider import ProviderGenerator
from hem.generators.report import ReportGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.paths import Paths
from hem.validators.asset_validator import AssetValidator


class BuildManager:

    def __init__(self, event_bus: EventBus | None = None):
        self.event_bus = event_bus or EventBus()

    def build(self) -> BuildContext:
        start_time = time.perf_counter()
        started_at = datetime.now()

        context = BuildContext()
        context.start_time = started_at
        context.manifest = BuildManifest(
            hem_version=context.version,
            started_at=started_at,
        )

        self.event_bus.emit("build_started", context)

        context.assets = AssetLoader(Paths.assets()).load()
        context.inventory = list(context.assets)
        context.statistics.assets_loaded = len(context.assets)
        self.event_bus.emit("assets_loaded", context.assets)

        AssetValidator().validate(context.assets)
        context.statistics.assets_validated = len(context.assets)
        self.event_bus.emit("assets_validated", context.assets)

        InventoryGenerator(Paths.templates()).generate(context)
        self.event_bus.emit("generator_finished", "InventoryGenerator")

        ProviderGenerator(Paths.templates()).generate(context)
        self.event_bus.emit("generator_finished", "ProviderGenerator")

        end_time = time.perf_counter()
        finished_at = datetime.now()
        context.finish_time = finished_at
        context.manifest.finished_at = finished_at
        context.statistics.build_time_ms = (end_time - start_time) * 1000

        ManifestGenerator(Paths.templates()).generate(context)
        self.event_bus.emit("generator_finished", "ManifestGenerator")

        self.event_bus.emit("build_finished", context)

        ReportGenerator().generate(context)

        return context
