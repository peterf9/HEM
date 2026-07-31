from pathlib import Path
from rich.console import Console

from hem.runtime.build_context import BuildContext

console = Console()


class ExplainManager:

    def explain(self, context: BuildContext, target_entity_id: str) -> None:
        if not context.manifest or not context.manifest.generated_entities:
            console.print("[red]No manifest or generated entities found in context.[/red]")
            return

        target = None
        for entity in context.manifest.generated_entities:
            if entity.entity_id.lower() == target_entity_id.lower():
                target = entity
                break

        if not target:
            console.print(f"[red]Entity '{target_entity_id}' not found in build manifest.[/red]")
            return

        console.print(f"\n[bold]Entity Explanation[/bold]: [bold green]{target.entity_id}[/bold green]\n")
        console.print(f"[bold]Platform:[/bold] {target.platform}")
        console.print(f"[bold]Generator / Provider:[/bold] {target.generator}")

        # Reverse lookup asset
        matching_asset = None
        for asset in context.inventory:
            if asset.id in target.entity_id:
                matching_asset = asset
                break

        if matching_asset:
            console.print(f"[bold]Asset ID:[/bold] {matching_asset.id} ({matching_asset.name})")
            console.print(f"[bold]Asset Class:[/bold] {matching_asset.class_name}")
            console.print(f"[bold]Location:[/bold] {matching_asset.location}")
            console.print(f"[bold]Source Availability:[/bold] {matching_asset.source.availability}")
            console.print(f"[bold]Source Latency:[/bold] {matching_asset.source.latency}")
        else:
            console.print("[bold]Asset ID:[/bold] [dim]System / Framework Telemetry Entity[/dim]")

        console.print()
