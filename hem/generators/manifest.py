import json

from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths


class ManifestGenerator(BaseGenerator):

    def generate(self, context: BuildContext) -> None:
        if not context.manifest:
            return

        output_dir = context.output_dir or Paths.hem_package_output()
        output_file = output_dir / "manifest.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        def to_relative_path(path):
            try:
                return str(path.relative_to(Paths.project_root()).as_posix())
            except ValueError:
                return str(path.as_posix())

        manifest_data = {
            "hem_version": context.manifest.hem_version,
            "manifest_version": context.manifest.manifest_version,
            "started_at": context.manifest.started_at.isoformat(),
            "finished_at": context.manifest.finished_at.isoformat() if context.manifest.finished_at else None,
            "generated_files": [to_relative_path(p) for p in context.manifest.generated_files],
            "generated_entities": [
                {
                    "entity_id": e.entity_id,
                    "platform": e.platform,
                    "generator": e.generator,
                }
                for e in context.manifest.generated_entities
            ],
            "statistics": {
                "assets_loaded": context.statistics.assets_loaded,
                "assets_validated": context.statistics.assets_validated,
                "entities_generated": context.statistics.entities_generated,
                "files_generated": context.statistics.files_generated,
                "warnings": context.statistics.warnings,
                "errors": context.statistics.errors,
                "build_time_ms": context.statistics.build_time_ms,
            },
        }

        output_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        context.manifest.generated_files.append(output_file)
        context.statistics.files_generated += 1
