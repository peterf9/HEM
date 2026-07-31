from hem.capabilities.power import PowerCapability


def test_power_capability():
    power = PowerCapability()
    assert power.metadata.name == "power"
    assert power.metadata.unit == "W"
    assert power.metadata.device_class == "power"
    assert power.metadata.icon == "mdi:flash"
