import typer

from rich import print

app = typer.Typer(
    help="HEM - HomeLab Enterprise Monitor"
)


@app.command()
def version():

    print("[green]HEM[/green] 0.1.0")


@app.command()
def doctor():

    print("[cyan]System OK[/cyan]")


@app.command()
def validate(path: str):
    """Validate an asset YAML file."""
    try:
        from hem.validators.asset_validator import validate_asset
        asset = validate_asset(path)
        print(f"[green]✓ Asset '{asset.name}' ({asset.id}) is valid![/green]")
    except Exception as e:
        print(f"[red]✗ Validation failed:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

