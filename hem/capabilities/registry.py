from typing import Dict, List, Type
from hem.capabilities.base import BaseCapability


class CapabilityRegistry:

    def __init__(self):
        self._capabilities: Dict[str, BaseCapability] = {}

    def register(self, capability: BaseCapability) -> None:
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> BaseCapability | None:
        return self._capabilities.get(name)

    def capabilities(self) -> List[BaseCapability]:
        return list(self._capabilities.values())
