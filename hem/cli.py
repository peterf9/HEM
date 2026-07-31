from pathlib import Path
import typer
from rich.console import Console

from hem.builders.build_manager import BuildManager
from hem.builders.deploy_manager import DeployManager
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
        manager.build()
    except Exception as e:
        console.print(f"[red]Build failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def deploy(target: str = typer.Option(None, help="Target Home Assistant packages directory")):
    try:
        target_path = Path(target) if target else None
        manager = DeployManager()
        manager.deploy(target_path)
    except Exception as e:
        console.print(f"[red]Deploy failed:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
