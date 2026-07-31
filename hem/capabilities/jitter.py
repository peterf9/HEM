from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class JitterCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="jitter",
            display_name="Jitter",
            description="Monitors network packet jitter",
            platform="sensor",
            unit="ms",
            icon="mdi:pulse",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Jitter"
        unique_id: "hem_{asset.id}_jitter"
        unit_of_measurement: "ms"
        state: >
          {{{{ states('{asset.source.jitter}') }}}}
"""
