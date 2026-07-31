from hem.capabilities.base import BaseCapability
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class NetworkBandwidthCapability(BaseCapability):

    @property
    def metadata(self) -> CapabilityMetadata:
        return CapabilityMetadata(
            name="bandwidth",
            display_name="Network Bandwidth Utilization",
            description="Monitors network interface throughput and bandwidth",
            platform="sensor",
            unit="Mbit/s",
            icon="mdi:swap-vertical-bold",
            state_class="measurement",
        )

    def render(self, context: BuildContext, asset: Asset) -> str:
        source_sensor = getattr(asset.source, "bandwidth", f"sensor.{asset.id}_bandwidth")
        return f"""  - sensor:
      - name: "HEM {asset.name} Bandwidth"
        unique_id: "hem_{asset.id}_bandwidth"
        unit_of_measurement: "Mbit/s"
        state: >
          {{{{ states('{source_sensor}') }}}}
"""
