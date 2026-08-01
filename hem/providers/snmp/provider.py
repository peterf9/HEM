from typing import List
from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.bandwidth import NetworkBandwidthCapability
from hem.capabilities.base import BaseCapability
from hem.capabilities.cpu import CpuCapability
from hem.capabilities.memory import MemoryCapability
from hem.capabilities.power import PowerCapability
from hem.capabilities.storage import StorageCapability
from hem.capabilities.temperature import TemperatureCapability
from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata


class SnmpProvider(BaseProvider):

    def __init__(self):
        self.capabilities_map = {
            "availability": AvailabilityCapability(),
            "cpu": CpuCapability(),
            "memory": MemoryCapability(),
            "bandwidth": NetworkBandwidthCapability(),
            "storage": StorageCapability(),
            "temperature": TemperatureCapability(),
            "power": PowerCapability(),
        }

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="snmp",
            version="1.3.0",
            author="HEM Core",
            description="Production SNMP Monitoring Provider for Switches, Routers, Storage, Power and Thermal Environment",
            capabilities=list(self.capabilities_map.keys()),
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "snmp"

    def get_capabilities(self, asset: Asset) -> List[BaseCapability]:
        return list(self.capabilities_map.values())
