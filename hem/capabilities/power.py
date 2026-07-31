from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class PowerCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="power",
            display_name="Power Consumption",
            description="Monitors hardware power consumption in Watts",
            platform="sensor",
            unit="W",
            icon="mdi:flash",
            device_class="power",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "power", f"sensor.{asset.id}_power")
        return f"""  - sensor:
      - name: "HEM {asset.name} Power Consumption"
        unique_id: "hem_{asset.id}_power"
        unit_of_measurement: "W"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
