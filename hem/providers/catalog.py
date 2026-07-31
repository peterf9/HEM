from dataclasses import dataclass
from typing import List
from hem.providers.base import BaseProvider


@dataclass
class CatalogEntry:
    name: str
    version: str
    description: str
    author: str
    capabilities: List[str]
    installed: bool = False


class ProviderCatalog:

    def __init__(self):
        self._entries: List[CatalogEntry] = [
            CatalogEntry("ping", "1.0.0", "Ping / Network availability and latency provider", "HEM Core", ["availability", "latency", "jitter", "packet_loss"], True),
            CatalogEntry("snmp", "0.1.0", "SNMP network device metrics provider", "Community", ["metrics", "availability"], False),
            CatalogEntry("rest", "0.1.0", "REST API JSON endpoint monitoring provider", "Community", ["metrics", "availability"], False),
            CatalogEntry("mqtt", "0.1.0", "MQTT broker sensor telemetry provider", "Community", ["metrics"], False),
            CatalogEntry("docker", "0.1.0", "Docker daemon container state provider", "Community", ["availability", "metrics"], False),
        ]

    def list_all(self) -> List[CatalogEntry]:
        return self._entries

    def search(self, query: str) -> List[CatalogEntry]:
        q = query.lower()
        return [e for e in self._entries if q in e.name.lower() or q in e.description.lower()]
