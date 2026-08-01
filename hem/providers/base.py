from abc import ABC, abstractmethod
from typing import List
from hem.capabilities.base import BaseCapability
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
    def get_capabilities(self, asset: Asset) -> List[BaseCapability]:
        """Returns the list of capability instances supported for this asset."""
        pass

    def generate(self, context: BuildContext, asset: Asset) -> None:
        """Default implementation is no-op as rendering is aggregated centrally in BuildManager."""
        pass
