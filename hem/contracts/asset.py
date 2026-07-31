from pydantic import BaseModel


class Source(BaseModel):
    availability: str
    latency: str
    jitter: str
    packet_loss: str


class Asset(BaseModel):
    id: str
    name: str
    provider: str
    class_name: str
    criticality: str
    source: Source
