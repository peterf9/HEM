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


if __name__ == "__main__":
    app()
