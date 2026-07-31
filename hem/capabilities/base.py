from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from hem.capabilities.metadata import CapabilityMetadata
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class BaseCapability(ABC):

    @property
    @abstractmethod
    def metadata(self) -> CapabilityMetadata:
        pass

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def platform(self) -> str:
        return self.metadata.platform

    @abstractmethod
    def render(self, context: BuildContext, asset: Asset) -> str:
        pass
