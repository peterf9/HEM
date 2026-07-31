from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class CpuCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="cpu",
            display_name="CPU Utilization",
            description="Monitors CPU utilization percentage",
            platform="sensor",
            unit="%",
            icon="mdi:cpu-64-bit",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "cpu", f"sensor.{asset.id}_cpu_utilization")
        return f"""  - sensor:
      - name: "HEM {asset.name} CPU Utilization"
        unique_id: "hem_{asset.id}_cpu"
        unit_of_measurement: "%"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
