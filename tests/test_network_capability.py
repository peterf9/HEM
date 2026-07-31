from hem.capabilities.bandwidth import NetworkBandwidthCapability


def test_network_bandwidth_capability():
    cap = NetworkBandwidthCapability()
    assert cap.metadata.name == "bandwidth"
    assert cap.metadata.unit == "Mbit/s"
    assert cap.metadata.icon == "mdi:swap-vertical-bold"
