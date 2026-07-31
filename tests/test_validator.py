import pytest
from hem.contracts.asset import Asset, Source
from hem.validators.asset_validator import AssetValidator


def test_asset_validator_success():
    asset1 = Asset(
        id="a1", name="A1", provider="ping", class_name="infra", criticality="low",
        source=Source(availability="b1", latency="s1", jitter="s2", packet_loss="s3")
    )
    asset2 = Asset(
        id="a2", name="A2", provider="ping", class_name="infra", criticality="low",
        source=Source(availability="b2", latency="s4", jitter="s5", packet_loss="s6")
    )
    validator = AssetValidator()
    validator.validate([asset1, asset2])


def test_asset_validator_duplicate_id():
    asset1 = Asset(
        id="a1", name="A1", provider="ping", class_name="infra", criticality="low",
        source=Source(availability="b1", latency="s1", jitter="s2", packet_loss="s3")
    )
    asset2 = Asset(
        id="a1", name="A1 Duplicate", provider="ping", class_name="infra", criticality="low",
        source=Source(availability="b2", latency="s4", jitter="s5", packet_loss="s6")
    )
    validator = AssetValidator()
    with pytest.raises(ValueError, match="Duplicate Asset ID: a1"):
        validator.validate([asset1, asset2])
