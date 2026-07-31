import json
from datetime import datetime

from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths


class InventoryGenerator(BaseGenerator):

    def generate(self, context: BuildContext) -> None:
        output_dir = context.output_dir or Paths.hem_package_output()
        output_file = output_dir / "inventory.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        inventory_data = {
            "hem_version": context.version,
            "inventory_version": 1,
            "generated_at": datetime.now().isoformat(),
            "total_assets": len(context.inventory),
            "assets": [
                {
                    "id": asset.id,
                    "name": asset.name,
                    "provider": asset.provider,
                    "class": asset.class_name,
                    "type": asset.type,
                    "vendor": asset.vendor,
                    "model": asset.model,
                    "firmware": asset.firmware,
                    "serial": asset.serial,
                    "location": asset.location,
                    "owner": asset.owner,
                    "criticality": asset.criticality,
                    "tags": asset.tags,
                    "description": asset.description,
                    "source": asset.source.model_dump(),
                }
                for asset in context.inventory
            ],
        }

        output_file.write_text(json.dumps(inventory_data, indent=2), encoding="utf-8")

        if context.manifest:
            context.manifest.generated_files.append(output_file)

        context.statistics.files_generated += 1
