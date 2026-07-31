from pydantic import BaseModel

from .source import Source


class Asset(BaseModel):

    id: str

    name: str

    provider: str

    class_name: str

    criticality: str

    source: Source
