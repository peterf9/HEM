from hem.builders.deploy_manager import DeployManager


def test_deploy_manager(tmp_path):
    target_dir = tmp_path / "ha_packages"
    manager = DeployManager()
    context = manager.deploy(target_dir=target_dir)

    assert target_dir.exists()
    deployed_files = list(target_dir.glob("*.yaml")) + list(target_dir.glob("*.json"))
    assert len(deployed_files) >= 1
    assert any(f.name == "templates.yaml" for f in deployed_files)
