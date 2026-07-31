from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class LatencyCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="latency",
            display_name="Latency",
            description="Monitors network round-trip latency",
            platform="sensor",
            unit="ms",
            icon="mdi:timer-outline",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - sensor:
      - name: "HEM {asset.name} Latency"
        unique_id: "hem_{asset.id}_latency"
        unit_of_measurement: "ms"
        state: >
          {{{{ states('{asset.source.latency}') }}}}
"""
