from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class RegistryGenerator(BaseGenerator):

    def generate(self, context: BuildContext) -> None:
        rendered = f"""template:
  - sensor:
      - name: "HEM Assets Total"
        unique_id: "hem_assets_total"
        state: >
          {context.statistics.assets_loaded}

      - name: "HEM Providers Total"
        unique_id: "hem_providers_total"
        state: >
          {len(context.statistics.providers_used)}

      - name: "HEM Build Duration"
        unique_id: "hem_build_duration"
        unit_of_measurement: "ms"
        state: >
          {context.statistics.build_time_ms:.2f}

      - name: "HEM Version"
        unique_id: "hem_version"
        state: >
          "{context.version}"
"""

        output_file = (context.output_dir or Paths.hem_package_output()) / "templates.yaml"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_file.exists():
            content = output_file.read_text(encoding="utf-8")
            if "hem_assets_total" not in content:
                content += "\n" + rendered
                output_file.write_text(content, encoding="utf-8")
        else:
            output_file.write_text(rendered, encoding="utf-8")

        if context.manifest and output_file not in context.manifest.generated_files:
            context.manifest.generated_files.append(output_file)

        if context.manifest:
            for sensor_id in ["hem_assets_total", "hem_providers_total", "hem_build_duration", "hem_version"]:
                context.manifest.generated_entities.append(
                    GeneratedEntity(
                        entity_id=f"sensor.{sensor_id}",
                        platform="sensor",
                        generator="RegistryGenerator",
                    )
                )

        context.statistics.entities_generated += 4
