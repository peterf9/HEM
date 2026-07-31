from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext


class SnmpProvider(BaseProvider):

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="snmp",
            version="0.1.0",
            author="Community",
            description="Snmp monitoring provider scaffold",
            capabilities=["availability"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "snmp"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        pass
