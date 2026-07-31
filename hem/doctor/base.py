from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from hem.runtime.build_context import BuildContext


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


class BaseCheck(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, context: BuildContext) -> CheckResult:
        pass
