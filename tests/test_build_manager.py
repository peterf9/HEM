from hem.builders.build_manager import BuildManager


def test_build_manager():
    manager = BuildManager()
    report = manager.build()

    assert report.asset_count > 0
    assert report.provider_count > 0
    assert report.template_count > 0
    assert len(report.generated_files) > 0
    assert report.generated_files[0].name == "provider.yaml"
    assert report.generated_files[0].exists()
