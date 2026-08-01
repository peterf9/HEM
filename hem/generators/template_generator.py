from typing import Dict, List
import yaml

from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class TemplateGenerator(BaseGenerator):
    """Centralized, deduplicated, Home Assistant-valid Template Generator."""

    def generate(self, context: BuildContext) -> None:
        pass

    def render_all(self, context: BuildContext, provider_capabilities: Dict[str, List[tuple]]) -> None:
        """
        provider_capabilities maps provider_name -> list of (asset, capability_instance)
        """
        templates_section: List[Dict] = []
        unique_ids = set()

        for provider_name, pairs in provider_capabilities.items():
            for asset, cap in pairs:
                unique_id = f"hem_{asset.id}_{cap.name}"
                if unique_id in unique_ids:
                    continue
                unique_ids.add(unique_id)

                cap_yaml = cap.render(context, asset)
                parsed = yaml.safe_load(cap_yaml)

                if parsed and isinstance(parsed, list):
                    for platform_block in parsed:
                        templates_section.append(platform_block)

        # Add Registry Generator sensors centrally
        registry_sensors = [
            {
                "sensor": [
                    {
                        "name": "HEM Assets Total",
                        "unique_id": "hem_assets_total",
                        "state": f"{{{{ {context.statistics.assets_loaded} }}}}",
                    },
                    {
                        "name": "HEM Providers Total",
                        "unique_id": "hem_providers_total",
                        "state": f"{{{{ {len(context.statistics.providers_used)} }}}}",
                    },
                    {
                        "name": "HEM Build Duration",
                        "unique_id": "hem_build_duration",
                        "unit_of_measurement": "ms",
                        "state": f"{{{{ {context.statistics.build_time_ms:.2f} }}}}",
                    },
                    {
                        "name": "HEM Version",
                        "unique_id": "hem_version",
                        "state": f'"{context.version}"',
                    },
                ]
            }
        ]

        full_lovelace_template = {
            "template": templates_section + registry_sensors
        }

        rendered = yaml.dump(full_lovelace_template, sort_keys=False)

        output_file = (context.output_dir or Paths.hem_package_output()) / "templates.yaml"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(rendered, encoding="utf-8")

        if context.manifest and output_file not in context.manifest.generated_files:
            context.manifest.generated_files.append(output_file)
