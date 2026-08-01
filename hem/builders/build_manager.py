from collections import defaultdict
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
from hem.generators.template_generator import TemplateGenerator
from hem.loaders.asset_loader import AssetLoader
from hem.providers.registry import ProviderRegistry
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import BuildManifest, GeneratedEntity
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

        # Centralized Capability Collection & Deduplication Map
        provider_capabilities = defaultdict(list)
        unique_entity_ids = set()

        for asset in context.assets:
            for provider in self.provider_registry.providers():
                if provider.supports(asset):
                    context.statistics.providers_used.add(provider.metadata.name)
                    capabilities = provider.get_capabilities(asset)
                    for cap in capabilities:
                        entity_id = f"{cap.platform}.hem_{asset.id}_{cap.name}"
                        if entity_id not in unique_entity_ids:
                            unique_entity_ids.add(entity_id)
                            provider_capabilities[provider.metadata.name].append((asset, cap))
                            if context.manifest:
                                context.manifest.generated_entities.append(
                                    GeneratedEntity(
                                        entity_id=entity_id,
                                        platform=cap.platform,
                                        generator=provider.__class__.__name__,
                                    )
                                )
                    self.event_bus.emit(GeneratorFinishedEvent(generator_name=provider.metadata.name))

        # Render deduplicated single-root template: package
        tpl_gen = TemplateGenerator(Paths.templates())
        tpl_gen.render_all(context, provider_capabilities)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="TemplateGenerator"))

        # Add Registry telemetry sensors to manifest
        if context.manifest:
            for sensor_id in ["hem_assets_total", "hem_providers_total", "hem_build_duration", "hem_version"]:
                context.manifest.generated_entities.append(
                    GeneratedEntity(
                        entity_id=f"sensor.{sensor_id}",
                        platform="sensor",
                        generator="RegistryGenerator",
                    )
                )

        DashboardGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="DashboardGenerator"))

        end_time = time.perf_counter()
        finished_at = datetime.now()
        context.finish_time = finished_at
        context.manifest.finished_at = finished_at
        context.statistics.build_time_ms = (end_time - start_time) * 1000
        context.statistics.entities_generated = len(context.manifest.generated_entities) if context.manifest else 0

        ManifestGenerator(Paths.templates()).generate(context)
        self.event_bus.emit(GeneratorFinishedEvent(generator_name="ManifestGenerator"))

        self.event_bus.emit(BuildFinishedEvent(context=context))

        ReportGenerator().generate(context)

        return context
