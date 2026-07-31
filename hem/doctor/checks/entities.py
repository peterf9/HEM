from hem.doctor.base import BaseCheck, CheckResult, CheckStatus
from hem.runtime.build_context import BuildContext


class EntitiesCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Entities Check"

    def run(self, context: BuildContext) -> CheckResult:
        if not context.manifest or not context.manifest.generated_entities:
            return CheckResult(
                check_name=self.name,
                passed=False,
                message="No entities generated in build context",
                recommendation="Verify that asset providers and capabilities are properly registered.",
                documentation="docs/troubleshooting/entities.md",
                status=CheckStatus.FAIL,
            )

        unique_ids = set()
        duplicates = []
        for entity in context.manifest.generated_entities:
            if entity.entity_id in unique_ids:
                duplicates.append(entity.entity_id)
            unique_ids.add(entity.entity_id)

        if duplicates:
            return CheckResult(
                check_name=self.name,
                passed=False,
                message=f"Duplicate entity IDs found: {', '.join(duplicates)}",
                recommendation="Ensure all asset IDs and entity unique_ids are unique across all YAML definitions.",
                documentation="docs/troubleshooting/entities.md",
                details={"duplicates": duplicates},
                status=CheckStatus.FAIL,
            )

        return CheckResult(
            check_name=self.name,
            passed=True,
            message=f"All {len(unique_ids)} generated entities are unique and valid",
            details={"total_entities": len(unique_ids)},
            status=CheckStatus.PASS,
        )
