from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class MemoryCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="memory",
            display_name="Memory Utilization",
            description="Monitors RAM memory utilization percentage",
            platform="sensor",
            unit="%",
            icon="mdi:memory",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "memory", f"sensor.{asset.id}_memory_utilization")
        return f"""  - sensor:
      - name: "HEM {asset.name} Memory Utilization"
        unique_id: "hem_{asset.id}_memory"
        unit_of_measurement: "%"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
