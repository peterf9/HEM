from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class ProviderGenerator(BaseGenerator):

    def generate(self, context: BuildContext) -> None:
        template = self.env.get_template("providers/provider.j2")

        rendered = template.render(
            assets=context.assets
        )

        output_file = (context.output_dir or Paths.hem_package_output()) / "templates.yaml"
        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file.write_text(
            rendered,
            encoding="utf-8"
        )

        if context.manifest:
            context.manifest.generated_files.append(output_file)
            for asset in context.assets:
                context.manifest.generated_entities.append(
                    GeneratedEntity(
                        entity_id=f"binary_sensor.hem_{asset.id}_available",
                        platform="template",
                        generator="ProviderGenerator"
                    )
                )

        context.statistics.files_generated += 1
        context.statistics.entities_generated += len(context.assets)
