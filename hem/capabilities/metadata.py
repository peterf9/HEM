from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CapabilityMetadata:
    name: str
    display_name: str
    description: str
    platform: str
    unit: Optional[str] = None
    icon: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = None
