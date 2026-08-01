from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class AvailabilityCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="availability",
            display_name="Availability",
            description="Monitors network availability state",
            platform="binary_sensor",
            icon="mdi:connectivity",
            device_class="connectivity",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        return f"""  - binary_sensor:
      - name: "HEM {asset.name} Availability"
        unique_id: "hem_{asset.id}_availability"
        state: >
          {{{{ is_state('{asset.source.availability}', 'on') }}}}
"""
