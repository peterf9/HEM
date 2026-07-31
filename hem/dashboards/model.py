from dataclasses import dataclass, field
from typing import List


@dataclass
class DashboardCard:
    type: str
    title: str
    content: dict


@dataclass
class DashboardView:
    title: str
    path: str
    icon: str
    cards: List[DashboardCard] = field(default_factory=list)


@dataclass
class DashboardModel:
    title: str
    views: List[DashboardView] = field(default_factory=list)
