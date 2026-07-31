from typing import List
from rich.console import Console

from hem.doctor.base import BaseCheck, BuildHealth, CheckResult, CheckStatus
from hem.doctor.checks.entities import EntitiesCheck
from hem.doctor.checks.inventory import InventoryCheck
from hem.doctor.checks.manifest import ManifestCheck
from hem.runtime.build_context import BuildContext

console = Console()


class DoctorManager:

    def __init__(self, checks: List[BaseCheck] | None = None):
        self.checks = checks or [
            ManifestCheck(),
            InventoryCheck(),
            EntitiesCheck(),
        ]

    def diagnose(self, context: BuildContext) -> BuildHealth:
        health = BuildHealth()
        console.print("\n[bold]HEM Doctor Diagnostics[/bold]\n")

        score_penalty = 0
        for check in self.checks:
            res = check.run(context)
            health.results.append(res)

            if res.passed:
                console.print(f"[green]✓ {res.check_name}[/green]: {res.message}")
            else:
                score_penalty += 33
                console.print(f"[red]✗ {res.check_name}[/red]: {res.message}")
                if res.recommendation:
                    console.print(f"  [yellow]Recommendation:[/yellow] {res.recommendation}")
                if res.documentation:
                    console.print(f"  [dim]Docs:[/dim] {res.documentation}")

        health.score = max(0, 100 - score_penalty)
        if health.score == 100:
            health.status = "HEALTHY"
            console.print("\n[bold green]✓ System Status: HEALTHY (Score: 100/100)[/bold green]\n")
        else:
            health.status = "DEGRADED" if health.score > 50 else "UNHEALTHY"
            console.print(f"\n[bold red]✗ System Status: {health.status} (Score: {health.score}/100)[/bold red]\n")

        return health
