from hem.builders.build_manager import BuildManager
from hem.doctor.doctor_manager import DoctorManager


def test_doctor_manager():
    build_mgr = BuildManager()
    context = build_mgr.build()

    doc_mgr = DoctorManager()
    results = doc_mgr.diagnose(context)

    assert len(results) == 3
    assert all(r.passed for r in results)
