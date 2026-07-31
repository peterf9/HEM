from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from hem.runtime.build_context import BuildContext


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    message: str
    recommendation: Optional[str] = None
    documentation: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    status: CheckStatus = CheckStatus.PASS


@dataclass
class BuildHealth:
    score: int = 100
    status: str = "HEALTHY"
    results: list[CheckResult] = field(default_factory=list)


class BaseCheck(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, context: BuildContext) -> CheckResult:
        pass
