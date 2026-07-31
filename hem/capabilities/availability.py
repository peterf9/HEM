from hem.capabilities.base import BaseCapability
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class AvailabilityCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "availability"

    @property
    def platform(self) -> str:
        return "binary_sensor"

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - binary_sensor:
      - name: "HEM {asset.name} Available"
        unique_id: "hem_{asset.id}_available"
        state: >
          {{{{ is_state('{asset.source.availability}', 'on') }}}}
"""
