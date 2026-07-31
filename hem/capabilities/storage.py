from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class StorageCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="storage",
            display_name="Storage Utilization",
            description="Monitors disk/storage utilization percentage",
            platform="sensor",
            unit="%",
            icon="mdi:harddisk",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "storage", f"sensor.{asset.id}_storage_utilization")
        return f"""  - sensor:
      - name: "HEM {asset.name} Storage Utilization"
        unique_id: "hem_{asset.id}_storage"
        unit_of_measurement: "%"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
