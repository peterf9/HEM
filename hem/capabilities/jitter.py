from hem.capabilities.base import BaseCapability
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class JitterCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "jitter"

    @property
    def platform(self) -> str:
        return "sensor"

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Jitter"
        unique_id: "hem_{asset.id}_jitter"
        unit_of_measurement: "ms"
        state: >
          {{{{ states('{asset.source.jitter}') }}}}
"""
