from abc import ABC, abstractmethod
from typing import Any, Dict
from hem.contracts.asset import Asset
from hem.runtime.build_context import BuildContext


class BaseCapability(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def platform(self) -> str:
        pass

    @abstractmethod
    def render(self, context: BuildContext, asset: Asset) -> str:
        pass
