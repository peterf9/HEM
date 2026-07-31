from hem.builders.explain_manager import ExplainManager
from hem.builders.scaffold_manager import ScaffoldManager
from hem.runtime.build_context import BuildContext


def test_explain_manager():
    ctx = BuildContext()
    from hem.builders.build_manager import BuildManager
    ctx = BuildManager().build()

    em = ExplainManager()
    # Should run without error
    em.explain(ctx, "binary_sensor.hem_brume_availability")


def test_scaffold_manager():
    sm = ScaffoldManager()
    p_dir = sm.create_provider_scaffold("snmp")

    assert p_dir.exists()
    assert (p_dir / "provider.py").exists()
    assert (p_dir / "README.md").exists()
