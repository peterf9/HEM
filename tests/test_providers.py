from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.providers.ping import PingProvider
from hem.providers.registry import ProviderRegistry
from hem.runtime.build_context import BuildContext


class CustomDemoProvider(BaseProvider):

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="demo",
            version="0.1.0",
            author="Plugin Test",
            description="Demo plugin provider",
            capabilities=["metrics"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "demo"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        pass


def test_provider_registry():
    registry = ProviderRegistry()
    registry.register(PingProvider())
    registry.register(CustomDemoProvider())

    assert len(registry.providers()) == 2
    assert registry.get("ping") is not None
    assert registry.get("demo") is not None
    assert registry.get("nonexistent") is None


def test_provider_discovery():
    registry = ProviderRegistry()
    registry.discover()
    assert any(p.metadata.name == "ping" for p in registry.providers())
