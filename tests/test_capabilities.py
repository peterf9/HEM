from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.latency import LatencyCapability
from hem.capabilities.registry import CapabilityRegistry
from hem.contracts.asset import Asset, Source
from hem.providers.ping import PingProvider
from hem.runtime.build_context import BuildContext


def test_capability_engine():
    registry = CapabilityRegistry()
    registry.register(AvailabilityCapability())
    registry.register(LatencyCapability())

    assert len(registry.capabilities()) == 2
    assert registry.get("availability") is not None
    assert registry.get("latency") is not None


def test_ping_provider_capabilities():
    provider = PingProvider()
    assert len(provider.capability_instances) == 4

    asset = Asset(
        id="test_router",
        name="Test Router",
        provider="ping",
        class_name="infra",
        criticality="high",
        source=Source(
            availability="binary_sensor.net_test",
            latency="sensor.net_test_latency",
            jitter="sensor.net_test_jitter",
            packet_loss="sensor.net_test_loss",
        ),
    )

    context = BuildContext()
    provider.generate(context, asset)

    assert context.statistics.entities_generated == 4
    assert len(context.manifest.generated_entities) == 4
    assert any(e.entity_id == "binary_sensor.hem_test_router_availability" for e in context.manifest.generated_entities)
    assert any(e.entity_id == "sensor.hem_test_router_latency" for e in context.manifest.generated_entities)
