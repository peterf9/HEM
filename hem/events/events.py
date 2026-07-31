from dataclasses import dataclass
from typing import List
from hem.contracts.asset import Asset


class Event:
    pass


@dataclass
class BuildStartedEvent(Event):
    context: any


@dataclass
class AssetsLoadedEvent(Event):
    assets: List[Asset]


@dataclass
class AssetsValidatedEvent(Event):
    assets: List[Asset]


@dataclass
class GeneratorFinishedEvent(Event):
    generator_name: str


@dataclass
class BuildFinishedEvent(Event):
    context: any
