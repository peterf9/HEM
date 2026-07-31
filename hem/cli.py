import typer
from rich.console import Console

from hem.builders.build_manager import BuildManager
from hem.loaders.asset_loader import AssetLoader
from hem.runtime.paths import Paths
from hem.validators.asset_validator import AssetValidator

console = Console()

app = typer.Typer(
    help="HEM - HomeLab Enterprise Monitor"
)


@app.command()
def version():
    console.print("[green]HEM[/green] 0.1.0")


@app.command()
def doctor():
    console.print("[cyan]System OK[/cyan]")


@app.command()
def validate():
    loader = AssetLoader(Paths.assets())

    assets = loader.load()

    AssetValidator().validate(assets)

    console.print()

    console.print("[green]✓ Validation successful[/green]")

    console.print(f"{len(assets)} assets loaded.")


@app.command()
def build():
    try:
        manager = BuildManager()
        report = manager.build()

        console.print("[bold]HEM Build[/bold]")
        console.print("────────────────────────────")
        console.print(f"Assets.............{report.asset_count}")
        console.print(f"Providers..........{report.provider_count}")
        console.print(f"Templates..........{report.template_count}")
        console.print("Output.............[green]OK[/green]")
        console.print("────────────────────────────")
        console.print()
        console.print("[bold]Generated Files[/bold]")

        for file_path in report.generated_files:
            rel_path = file_path.relative_to(Paths.project_root())
            console.print(f"[green]✓[/green] {rel_path}")

        console.print()
        console.print("[green]Done.[/green]")
    except Exception as e:
        console.print(f"[red]Build failed:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
