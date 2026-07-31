from hem.builders.init_manager import InitManager


def test_init_manager(tmp_path):
    target = InitManager().initialize_project(root_dir=tmp_path)

    assert (target / "src" / "assets").exists()
    assert (target / "src" / "providers").exists()
    assert (target / "output").exists()
    assert (target / "docs").exists()
    assert (target / "src" / "assets" / "sample_gateway.yaml").exists()
