from hem.doctor.base import BaseCheck, CheckResult, CheckStatus
from hem.runtime.build_context import BuildContext


class ManifestCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Manifest Check"

    def run(self, context: BuildContext) -> CheckResult:
        if not context.manifest:
            return CheckResult(
                check_name=self.name,
                passed=False,
                message="Manifest not found in BuildContext",
                recommendation="Run 'hem build' to generate the manifest before running doctor.",
                documentation="docs/troubleshooting/manifest.md",
                status=CheckStatus.FAIL,
            )

        return CheckResult(
            check_name=self.name,
            passed=True,
            message=f"Manifest v{context.manifest.manifest_version} valid (HEM v{context.manifest.hem_version})",
            details={"generated_files": len(context.manifest.generated_files)},
            status=CheckStatus.PASS,
        )
