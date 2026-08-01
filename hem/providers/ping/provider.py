from typing import List
from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.base import BaseCapability
from hem.capabilities.jitter import JitterCapability
from hem.capabilities.latency import LatencyCapability
from hem.capabilities.packet_loss import PacketLossCapability
from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity


class PingProvider(BaseProvider):

    def __init__(self):
        self.capability_instances: List[BaseCapability] = [
            AvailabilityCapability(),
            LatencyCapability(),
            JitterCapability(),
            PacketLossCapability(),
        ]

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="ping",
            version="1.0.0",
            author="HEM Core Team",
            description="Ping / Network capability-based monitoring provider",
            capabilities=["availability", "latency", "jitter", "packet_loss"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "ping"

    def get_capabilities(self, asset: Asset) -> List[BaseCapability]:
        return self.capability_instances
