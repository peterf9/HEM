from hem.doctor.base import BaseCheck, CheckResult, CheckStatus
from hem.runtime.build_context import BuildContext


class InventoryCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Inventory Check"

    def run(self, context: BuildContext) -> CheckResult:
        count = len(context.inventory)
        if count == 0:
            return CheckResult(
                check_name=self.name,
                passed=False,
                message="Inventory is empty",
                recommendation="Add asset definition YAML files into 'src/assets/' directory.",
                documentation="docs/troubleshooting/inventory.md",
                status=CheckStatus.FAIL,
            )

        return CheckResult(
            check_name=self.name,
            passed=True,
            message=f"Inventory contains {count} validated assets",
            details={"total_assets": count},
            status=CheckStatus.PASS,
        )
