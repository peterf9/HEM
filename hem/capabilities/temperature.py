from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class TemperatureCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="temperature",
            display_name="Temperature",
            description="Monitors hardware component temperature in degrees Celsius",
            platform="sensor",
            unit="°C",
            icon="mdi:thermometer",
            device_class="temperature",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "temperature", f"sensor.{asset.id}_temperature")
        return f"""  - sensor:
      - name: "HEM {asset.name} Temperature"
        unique_id: "hem_{asset.id}_temperature"
        unit_of_measurement: "°C"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
