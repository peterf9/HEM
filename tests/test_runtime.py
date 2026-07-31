from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import BuildManifest
from hem.runtime.statistics import BuildStatistics
from hem.contracts.asset import Asset, Source


def test_build_context():
    context = BuildContext()
    asset = Asset(
        id="test", name="Test", provider="ping", class_name="infra", criticality="low",
        source=Source(availability="b1", latency="s1", jitter="s2", packet_loss="s3")
    )
    context.assets.append(asset)
    context.statistics.record_assets(context.assets)
    
    assert context.statistics.total_assets == 1
    assert context.statistics.total_providers == 1
    assert "ping" in context.statistics.providers_used
