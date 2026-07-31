from pathlib import Path
from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths


class DocumentationGenerator(BaseGenerator):

    def generate(self, context: BuildContext) -> None:
        docs_dir = Paths.project_root() / "docs" / "generated"
        docs_dir.mkdir(parents=True, exist_ok=True)

        # 1. inventory.md
        inv_content = f"# System Inventory Documentation\n\n- **Generated At**: {context.finish_time}\n- **Total Assets**: {len(context.inventory)}\n\n## Assets List\n\n"
        for a in context.inventory:
            inv_content += f"### {a.name} (`{a.id}`)\n- **Provider**: {a.provider}\n- **Class**: {a.class_name}\n- **Location**: {a.location}\n- **Criticality**: {a.criticality}\n\n"
        (docs_dir / "inventory.md").write_text(inv_content, encoding="utf-8")

        # 2. entities.md
        ent_content = f"# Generated Entities Documentation\n\n- **Total Entities**: {context.statistics.entities_generated}\n\n| Entity ID | Platform | Generator |\n| --- | --- | --- |\n"
        if context.manifest:
            for e in context.manifest.generated_entities:
                ent_content += f"| `{e.entity_id}` | `{e.platform}` | `{e.generator}` |\n"
        (docs_dir / "entities.md").write_text(ent_content, encoding="utf-8")

        # 3. providers.md
        prov_content = f"# Registered Providers Documentation\n\n| Provider | Version | Description | Capabilities |\n| --- | --- | --- | --- |\n"
        from hem.providers.registry import ProviderRegistry
        reg = ProviderRegistry()
        reg.discover()
        for p in reg.providers():
            m = p.metadata
            prov_content += f"| `{m.name}` | `v{m.version}` | {m.description} | `{', '.join(m.capabilities)}` |\n"
        (docs_dir / "providers.md").write_text(prov_content, encoding="utf-8")

        # 4. build.md
        build_content = f"# Build Engine Metrics\n\n- **Assets Loaded**: {context.statistics.assets_loaded}\n- **Entities Generated**: {context.statistics.entities_generated}\n- **Files Generated**: {context.statistics.files_generated}\n- **Build Time**: {context.statistics.build_time_ms:.2f}ms\n"
        (docs_dir / "build.md").write_text(build_content, encoding="utf-8")

        if context.manifest:
            context.manifest.generated_files.extend([
                docs_dir / "inventory.md",
                docs_dir / "entities.md",
                docs_dir / "providers.md",
                docs_dir / "build.md",
            ])

        context.statistics.files_generated += 4
