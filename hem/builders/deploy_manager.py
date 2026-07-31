from pathlib import Path
from rich.console import Console

from hem.builders.build_manager import BuildManager
from hem.runtime.build_context import BuildContext
from hem.services.deploy_service import DeployService

console = Console()


class DeployManager:

    def __init__(self):
        self.build_manager = BuildManager()
        self.deploy_service = DeployService()

    def deploy(self, target_dir: Path | None = None) -> BuildContext:
        context = self.build_manager.build()

        deploy_target = target_dir or (Path.cwd() / "output" / "deploy")

        console.print("\n[bold]HEM Deployer[/bold]\n")
        deployed_files = self.deploy_service.deploy(context, deploy_target)

        for df in deployed_files:
            console.print(f"[green]✓ Deployed {df.name}[/green] -> {df}")

        console.print("\n[bold green]✓ Deploy successful[/bold green]\n")
        return context
