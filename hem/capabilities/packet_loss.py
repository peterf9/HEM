from hem.capabilities.base import BaseCapability
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class PacketLossCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "packet_loss"

    @property
    def platform(self) -> str:
        return "sensor"

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Packet Loss"
        unique_id: "hem_{asset.id}_packet_loss"
        unit_of_measurement: "%"
        state: >
          {{{{ states('{asset.source.packet_loss}') }}}}
"""
