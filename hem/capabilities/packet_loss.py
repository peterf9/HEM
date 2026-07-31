from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class PacketLossCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="packet_loss",
            display_name="Packet Loss",
            description="Monitors network packet loss percentage",
            platform="sensor",
            unit="%",
            icon="mdi:package-variant-remove",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Packet Loss"
        unique_id: "hem_{asset.id}_packet_loss"
        unit_of_measurement: "%"
        state: >
          {{{{ states('{asset.source.packet_loss}') }}}}
"""
