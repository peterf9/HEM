from hem.doctor.base import BaseCheck, CheckResult
from hem.runtime.build_context import BuildContext


class EntitiesCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Entities Check"

    def run(self, context: BuildContext) -> CheckResult:
        if not context.manifest or not context.manifest.generated_entities:
            return CheckResult(self.name, False, "No entities generated in build context")

        unique_ids = set()
        duplicates = []
        for entity in context.manifest.generated_entities:
            if entity.entity_id in unique_ids:
                duplicates.append(entity.entity_id)
            unique_ids.add(entity.entity_id)

        if duplicates:
            return CheckResult(
                self.name,
                False,
                f"Duplicate entity IDs found: {', '.join(duplicates)}",
                {"duplicates": duplicates}
            )

        return CheckResult(
            self.name,
            True,
            f"All {len(unique_ids)} generated entities are unique and valid",
            {"total_entities": len(unique_ids)}
        )
