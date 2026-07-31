import time
from datetime import datetime

from hem.events.event_bus import EventBus
from hem.events.events import (
    BuildStartedEvent,
    AssetsLoadedEvent,
    AssetsValidatedEvent,
    GeneratorFinishedEvent,
    BuildFinishedEvent,
)
from hem.generators.dashboard import DashboardGenerator
from hem.generators.inventory import InventoryGenerator
from hem.generators.manifest import ManifestGenerator
from hem.generators.registry import RegistryGenerator
from hem.generators.report import ReportGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.providers.registry import ProviderRegistry
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.paths import Paths
from hem.validators.asset_validator import AssetValidator


class BuildManager:

    def __init__(self, event_bus: EventBus | None = None, provider_registry: ProviderRegistry | None = None):
        self.event_bus = event_bus or EventBus()
        self.provider_registry = provider_registry or ProviderRegistry()
        self.provider_registry.discover()

    def build(self) -> BuildContext:
        start_time = time.perf_counter()
        started_at = datetime.now()

        context = BuildContext()
        context.start_time = started_at
        context.manifest = BuildManifest(
            hem_version=context.version,
            started_at=started_at,
        )

        self.event_bus.emit(BuildStartedEvent(context=context))

        context.assets = AssetLoader(Paths.assets()).load()
        context.inventory = list(context.assets)
        context.statistics.assets_loaded = len(context.assets)
        self.event_bus.emit(AssetsLoadedEvent(assets=context.assets))

        AssetValidator().validate(context.assets)
        context.statistics.assets_validated = len(context.assets)
        self.event_bus.emit(AssetsValidatedEvent(assets=context.assets))

        InventoryGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="InventoryGenerator"))

        for asset in context.assets:
            for provider in self.provider_registry.providers():
                if provider.supports(asset):
                    provider.generate(context, asset)
                    context.statistics.providers_used.add(provider.metadata.name)
                    self.event_bus.emit(GeneratorFinishedEvent(generator_name=provider.metadata.name))

        RegistryGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="RegistryGenerator"))

        DashboardGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="DashboardGenerator"))

        end_time = time.perf_counter()
        finished_at = datetime.now()
        context.finish_time = finished_at
        context.manifest.finished_at = finished_at
        context.statistics.build_time_ms = (end_time - start_time) * 1000

        ManifestGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="ManifestGenerator"))

        self.event_bus.emit(BuildFinishedEvent(context=context))

        ReportGenerator().generate(context)

        return context
