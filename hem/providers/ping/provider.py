from typing import List, Type
from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.base import BaseCapability
from hem.capabilities.jitter import JitterCapability
from hem.capabilities.latency import LatencyCapability
from hem.capabilities.packet_loss import PacketLossCapability
from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class PingProvider(BaseProvider):

    def __init__(self):
        self.capability_instances: List[BaseCapability] = [
            AvailabilityCapability(),
            LatencyCapability(),
            JitterCapability(),
            PacketLossCapability(),
        ]

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="ping",
            version="1.0.0",
            author="HEM Core Team",
            description="Ping / Network capability-based monitoring provider",
            capabilities=["availability", "latency", "jitter", "packet_loss"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "ping"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        if not self.supports(asset):
            return

        rendered_sections = []
        for cap in self.capability_instances:
            rendered_sections.append(cap.render(context, asset))

        rendered = "template:\n" + "\n".join(rendered_sections)

        output_file = (context.output_dir or Paths.hem_package_output()) / "templates.yaml"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_file.exists():
            content = output_file.read_text(encoding="utf-8")
            if f"hem_{asset.id}_available" not in content:
                content += "\n" + rendered
                output_file.write_text(content, encoding="utf-8")
        else:
            output_file.write_text(rendered, encoding="utf-8")

        if context.manifest and output_file not in context.manifest.generated_files:
            context.manifest.generated_files.append(output_file)

        if context.manifest:
            for cap in self.capability_instances:
                context.manifest.generated_entities.append(
                    GeneratedEntity(
                        entity_id=f"{cap.platform}.hem_{asset.id}_{cap.name}",
                        platform=cap.platform,
                        generator="PingProvider",
                    )
                )

        context.statistics.files_generated = len(context.manifest.generated_files) if context.manifest else 1
        context.statistics.entities_generated += len(self.capability_instances)
