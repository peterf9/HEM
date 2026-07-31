from typing import List
from rich.console import Console

from hem.doctor.base import BaseCheck, CheckResult
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

    def diagnose(self, context: BuildContext) -> List[CheckResult]:
        results = []
        console.print("\n[bold]HEM Doctor[/bold]\n")

        all_passed = True
        for check in self.checks:
            res = check.run(context)
            results.append(res)
            if res.passed:
                console.print(f"[green]✓ {res.check_name}[/green]: {res.message}")
            else:
                all_passed = False
                console.print(f"[red]✗ {res.check_name}[/red]: {res.message}")

        console.print()
        if all_passed:
            console.print("[bold green]✓ System OK[/bold green]\n")
        else:
            console.print("[bold red]✗ Issues detected[/bold red]\n")

        return results
