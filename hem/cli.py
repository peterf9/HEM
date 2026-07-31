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
    try:
        manager = BuildManager()
        context = manager.build()
        from hem.doctor.doctor_manager import DoctorManager
        DoctorManager().diagnose(context)
    except Exception as e:
        console.print(f"[red]Doctor diagnosis failed:[/red] {e}")
        raise typer.Exit(code=1)


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
def plan():
    """Preview changes and impact before deployment."""
    try:
        from hem.builders.plan_manager import PlanManager
        from hem.runtime.paths import Paths

        pm = PlanManager()
        diff = pm.plan()

        console.print("\n[bold]HEM Execution Plan[/bold]\n")
        console.print(f"[bold green]Assets:[/bold green] {len(diff.new_assets)} assets to compile ({', '.join(diff.new_assets)})")
        console.print(f"[bold green]Entities:[/bold green] +{len(diff.new_entities)} entities generated")
        console.print(f"[bold green]Files:[/bold green] {len(diff.new_files)} target files")

        for f in diff.new_files:
            try:
                rel = f.relative_to(Paths.project_root()).as_posix()
            except ValueError:
                rel = str(f)
            console.print(f"  [dim]• {rel}[/dim]")

        console.print("\n[bold green]✓ Plan execution safe. Ready for 'hem deploy'[/bold green]\n")
    except Exception as e:
        console.print(f"[red]Plan failed:[/red] {e}")
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


@app.command()
def providers():
    """List registered monitoring providers."""
    from hem.providers.registry import ProviderRegistry
    registry = ProviderRegistry()
    registry.discover()
    
    console.print("\n[bold]Registered Providers[/bold]\n")
    for provider in registry.providers():
        meta = provider.metadata
        console.print(f"[bold green]• {meta.name}[/bold green] (v{meta.version}) - {meta.description}")
        console.print(f"  [dim]Capabilities:[/dim] {', '.join(meta.capabilities)}")
    console.print()


@app.command()
def search(query: str = typer.Argument("", help="Search query for providers catalog")):
    """Search for providers in the HEM catalog."""
    from hem.providers.catalog import ProviderCatalog
    cat = ProviderCatalog()
    results = cat.search(query)

    console.print(f"\n[bold]Provider Catalog Search[/bold] (Query: '{query}')\n")
    for entry in results:
        status_str = "[green][Installed][/green]" if entry.installed else "[dim][Available][/dim]"
        console.print(f"{status_str} [bold green]{entry.name}[/bold green] (v{entry.version}) - {entry.description}")
        console.print(f"  [dim]Author:[/dim] {entry.author} | [dim]Capabilities:[/dim] {', '.join(entry.capabilities)}")
    console.print()


@app.command()
def sdk_validate(name: str = typer.Argument("ping", help="Provider name to validate against SDK")):
    """Validate a provider implementation against Provider SDK specifications."""
    try:
        from hem.providers.registry import ProviderRegistry
        from hem.providers.validator import ProviderSDKValidator

        registry = ProviderRegistry()
        registry.discover()
        provider = registry.get(name)

        if not provider:
            console.print(f"[red]Provider '{name}' not found.[/red]")
            raise typer.Exit(code=1)

        validator = ProviderSDKValidator()
        res = validator.validate(provider)

        console.print(f"\n[bold]HEM Provider SDK Validation[/bold]: [bold green]{res.provider_name}[/bold green]\n")
        for item in res.items:
            icon = "[green]✓[/green]" if item.passed else "[red]✗[/red]"
            console.print(f"{icon} [bold]{item.check}[/bold]: {item.message}")

        console.print(f"\n[bold green]Provider Score: {res.score}/100[/bold green]\n")
    except Exception as e:
        console.print(f"[red]SDK Validation failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def docgen():
    """Generate Markdown documentation for inventory and entities."""
    try:
        manager = BuildManager()
        context = manager.build()
        from hem.generators.documentation import DocumentationGenerator
        doc_gen = DocumentationGenerator(Paths.templates())
        doc_gen.generate(context)
        console.print("\n[bold green]✓ Markdown Documentation generated successfully in docs/generated/[/bold green]\n")
    except Exception as e:
        console.print(f"[red]Docgen failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def explain(entity_id: str = typer.Argument(..., help="Entity ID to explain")):
    """Explain provenance and generation details for a specific entity."""
    try:
        manager = BuildManager()
        context = manager.build()
        from hem.builders.explain_manager import ExplainManager
        ExplainManager().explain(context, entity_id)
    except Exception as e:
        console.print(f"[red]Explain failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def new(name: str = typer.Argument(..., help="Provider extension name to scaffold")):
    """Scaffold a new provider extension package."""
    try:
        from hem.builders.scaffold_manager import ScaffoldManager
        p_dir = ScaffoldManager().create_provider_scaffold(name)
        console.print(f"\n[bold green]✓ Provider '{name}' scaffolded successfully at {p_dir}[/bold green]\n")
    except Exception as e:
        console.print(f"[red]Scaffold failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def init():
    """Initialize a new HEM user project structure and sample assets."""
    try:
        from hem.builders.init_manager import InitManager
        target = InitManager().initialize_project()
        console.print(f"\n[bold green]✓ HEM Project initialized successfully at {target}[/bold green]\n")
        console.print("  [dim]Created:[/dim] src/assets/, src/providers/, output/, docs/")
        console.print("  [dim]Sample Asset:[/dim] src/assets/sample_gateway.yaml\n")
        console.print("Run [bold cyan]hem build[/bold cyan] to perform your first build!\n")
    except Exception as e:
        console.print(f"[red]Init failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def graph():
    """Generate a Mermaid dependency graph of assets, providers, and entities."""
    try:
        manager = BuildManager()
        context = manager.build()
        from hem.builders.graph_manager import GraphManager
        gm = GraphManager()
        mermaid_code = gm.generate_mermaid(context)

        console.print("\n[bold]HEM System Dependency Graph (Mermaid)[/bold]\n")
        console.print(f"```mermaid\n{mermaid_code}\n```\n")
    except Exception as e:
        console.print(f"[red]Graph generation failed:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def verify():
    """Run full pre-deploy verification battery across build, doctor, and SDK validation."""
    try:
        from hem.builders.verification_manager import VerificationManager
        vm = VerificationManager()
        success = vm.verify()

        if success:
            console.print("\n[bold green]✓ Pre-deploy Verification SUCCESSFUL! All build, doctor, and SDK checks passed.[/bold green]\n")
        else:
            console.print("\n[bold red]✗ Pre-deploy Verification FAILED. Fix issues before deployment.[/bold red]\n")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Verify failed:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()





