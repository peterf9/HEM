from hem.builders.verification_manager import VerificationManager


def test_verification_manager():
    vm = VerificationManager()
    success = vm.verify()

    assert success is True
