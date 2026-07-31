from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.runtime.build_context import BuildContext
from hem.runtime.metrics import MetricsCollector


def test_capability_metadata():
    cap = AvailabilityCapability()
    meta = cap.metadata

    assert isinstance(meta, CapabilityMetadata)
    assert meta.name == "availability"
    assert meta.display_name == "Availability"
    assert meta.icon == "mdi:connectivity"
    assert meta.device_class == "connectivity"


def test_metrics_api():
    from hem.builders.build_manager import BuildManager
    ctx = BuildManager().build()

    metrics = MetricsCollector.collect(ctx)
    assert metrics.assets_count == 1
    assert metrics.health_score == 100
    assert metrics.health_status == "HEALTHY"
