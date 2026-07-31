from rich.console import Console

from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths

console = Console()


class ReportGenerator:

    def generate(self, context: BuildContext) -> None:
        console.print("[bold]HEM Builder[/bold]\n")

        console.print(f"[green]✓ Assets loaded ({context.statistics.assets_loaded})[/green]")
        console.print(f"[green]✓ Assets validated ({context.statistics.assets_validated})[/green]")
        console.print(f"[green]✓ Inventory compiled ({len(context.inventory)} assets)[/green]")
        console.print("[green]✓ Provider compiled[/green]")

        if context.manifest:
            for file_path in context.manifest.generated_files:
                try:
                    rel_path = file_path.relative_to(Paths.project_root()).as_posix()
                except ValueError:
                    rel_path = str(file_path)
                console.print(f"[green]✓ {file_path.name} generated[/green] ({rel_path})")

        console.print()
        console.print("[bold green]✓ Build successful[/bold green]\n")

        console.print("────────────────────────────")
        console.print(f"Assets.............{context.statistics.assets_loaded}")
        console.print(f"Entities...........{context.statistics.entities_generated}")
        console.print(f"Files..............{context.statistics.files_generated}")
        console.print(f"Build Time.........{context.statistics.build_time_ms:.2f}ms")
        console.print("Output.............[green]OK[/green]")
        console.print("────────────────────────────\n")
        console.print("[green]Done.[/green]")
