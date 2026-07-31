from rich.console import Console

from hem.runtime.build_context import BuildContext

console = Console()


class GraphManager:

    def generate_mermaid(self, context: BuildContext) -> str:
        lines = [
            "graph TD",
            "    subgraph Assets",
        ]

        for asset in context.inventory:
            lines.append(f"        asset_{asset.id}[\"Asset: {asset.name} ({asset.id})\"]")

        lines.append("    end")
        lines.append("    subgraph Providers")

        from hem.providers.registry import ProviderRegistry
        reg = ProviderRegistry()
        reg.discover()
        for p in reg.providers():
            lines.append(f"        provider_{p.metadata.name}[\"Provider: {p.metadata.name} (v{p.metadata.version})\"]")

        lines.append("    end")
        lines.append("    subgraph Generated Entities")

        if context.manifest:
            for entity in context.manifest.generated_entities:
                clean_id = entity.entity_id.replace(".", "_")
                lines.append(f"        entity_{clean_id}[\"{entity.entity_id}\"]")

        lines.append("    end")

        # Connect assets to providers
        for asset in context.inventory:
            lines.append(f"    asset_{asset.id} --> provider_{asset.provider}")

        # Connect providers to entities
        if context.manifest:
            for entity in context.manifest.generated_entities:
                clean_id = entity.entity_id.replace(".", "_")
                gen_name = entity.generator.replace("Provider", "").lower()
                lines.append(f"    provider_{gen_name} --> entity_{clean_id}")

        mermaid_str = "\n".join(lines)
        return mermaid_str
