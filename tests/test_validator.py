from hem.validators.asset_validator import validate_asset


def test_validate_asset_brume():
    asset = validate_asset("src/assets/brume.yaml")
    assert asset.id == "brume"
    assert asset.name == "Brume"
    assert asset.provider == "ping"
    assert asset.criticality == "critical"
