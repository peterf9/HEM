from hem.capabilities.base import BaseCapability
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class LatencyCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "latency"

    @property
    def platform(self) -> str:
        return "sensor"

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Latency"
        unique_id: "hem_{asset.id}_latency"
        unit_of_measurement: "ms"
        state: >
          {{{{ states('{asset.source.latency}') }}}}
"""
