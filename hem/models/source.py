from pydantic import BaseModel


class Source(BaseModel):

    availability: str

    latency: str

    jitter: str

    packet_loss: str
