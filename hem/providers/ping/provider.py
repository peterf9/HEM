from hem.runtime.build_manifest import GeneratedEntity
from pathlib import Path
from hem.contracts.asset import Asset
from hem.generators.base import BaseGenerator
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths


class PingProvider(BaseProvider, BaseGenerator):

    def __init__(self, template_path: Path | None = None):
        BaseGenerator.__init__(self, template_path or Paths.templates())

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="ping",
            version="1.0.0",
            author="HEM Core Team",
            description="Ping / Network availability and latency monitoring provider",
            capabilities=["availability", "latency", "jitter", "packet_loss"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "ping"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        if not self.supports(asset):
            return

        template = self.env.get_template("providers/provider.j2")
        rendered = template.render(assets=[asset])

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
            context.manifest.generated_entities.append(
                GeneratedEntity(
                    entity_id=f"binary_sensor.hem_{asset.id}_available",
                    platform="template",
                    generator="PingProvider",
                )
            )

        context.statistics.files_generated = len(context.manifest.generated_files) if context.manifest else 1
        context.statistics.entities_generated += 1
