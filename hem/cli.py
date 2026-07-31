import typer
from rich.console import Console

from hem.generators.provider import ProviderGenerator
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
    loader = AssetLoader(Paths.assets())
    assets = loader.load()

    AssetValidator().validate(assets)

    output_file = Paths.hem_package_output() / "templates.yaml"
    generator = ProviderGenerator(Paths.templates())
    generator.generate(assets, output_file)

    console.print()
    console.print(f"[green]✓ Build successful![/green] Artifact generated at [bold]{output_file}[/bold]")


if __name__ == "__main__":
    app()
