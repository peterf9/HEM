from hem.doctor.base import BaseCheck, CheckResult
from hem.runtime.build_context import BuildContext


class ManifestCheck(BaseCheck):

    @property
    def name(self) -> str:
        return "Manifest Check"

    def run(self, context: BuildContext) -> CheckResult:
        if not context.manifest:
            return CheckResult(self.name, False, "Manifest not found in BuildContext")
        
        return CheckResult(
            self.name,
            True,
            f"Manifest v{context.manifest.manifest_version} valid (HEM v{context.manifest.hem_version})",
            {"generated_files": len(context.manifest.generated_files)}
        )
