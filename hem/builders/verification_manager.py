from hem.builders.build_manager import BuildManager
from hem.doctor.doctor_manager import DoctorManager
from hem.providers.registry import ProviderRegistry
from hem.providers.validator import ProviderSDKValidator


class VerificationManager:

    def verify(self) -> bool:
        # Step 1: Perform Build
        bm = BuildManager()
        context = bm.build()

        # Step 2: Perform Doctor Diagnostics
        doc_mgr = DoctorManager()
        health = doc_mgr.diagnose(context)
        if health.status == "UNHEALTHY":
            return False

        # Step 3: Perform SDK Validation on registered providers
        reg = ProviderRegistry()
        reg.discover()
        validator = ProviderSDKValidator()

        for p in reg.providers():
            res = validator.validate(p)
            if res.score < 100:
                return False

        return True
