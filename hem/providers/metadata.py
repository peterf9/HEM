from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ProviderMetadata:
    name: str
    version: str
    author: str
    description: str
    capabilities: List[str]
