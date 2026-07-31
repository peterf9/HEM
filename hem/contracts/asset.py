from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    availability: Optional[str] = None
    latency: Optional[str] = None
    jitter: Optional[str] = None
    packet_loss: Optional[str] = None
    cpu: Optional[str] = None
    memory: Optional[str] = None
    extra_fields: Dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "extra": "allow"
    }


class Asset(BaseModel):
    id: str
    name: str
    provider: str
    class_name: str = Field(alias="class", default="infrastructure")
    type: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    firmware: Optional[str] = None
    serial: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    criticality: str = "medium"
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    source: Source

    model_config = {
        "populate_by_name": True
    }
