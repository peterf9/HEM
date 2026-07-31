from abc import ABC, abstractmethod
from hem.contracts.asset import Asset
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext


class BaseProvider(ABC):

    @property
    @abstractmethod
    def metadata(self) -> ProviderMetadata:
        pass

    @abstractmethod
    def supports(self, asset: Asset) -> bool:
        pass

    @abstractmethod
    def generate(self, context: BuildContext, asset: Asset) -> None:
        pass
