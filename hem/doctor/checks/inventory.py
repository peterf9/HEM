from hem.doctor.base import BaseCheck, CheckResult
from hem.runtime.build_context import BuildContext


class InventoryCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Inventory Check"

    def run(self, context: BuildContext) -> CheckResult:
        count = len(context.inventory)
        if count == 0:
            return CheckResult(self.name, False, "Inventory is empty")

        return CheckResult(
            self.name,
            True,
            f"Inventory contains {count} validated assets",
            {"total_assets": count}
        )
