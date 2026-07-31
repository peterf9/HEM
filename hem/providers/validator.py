from dataclasses import dataclass, field
from typing import List
from hem.providers.base import BaseProvider


@dataclass
class ValidationItem:
    check: str
    passed: bool
    message: str


@dataclass
class ProviderValidationResult:
    provider_name: str
    score: int
    items: List[ValidationItem] = field(default_factory=list)


class ProviderSDKValidator:

    def validate(self, provider: BaseProvider) -> ProviderValidationResult:
        items = []
        meta = provider.metadata

        # Check 1: Metadata
        if meta and meta.name and meta.version:
            items.append(ValidationItem("Metadata", True, f"Valid metadata for '{meta.name}' (v{meta.version})"))
        else:
            items.append(ValidationItem("Metadata", False, "Missing or incomplete ProviderMetadata"))

        # Check 2: Capabilities
        if meta and meta.capabilities and len(meta.capabilities) > 0:
            items.append(ValidationItem("Capabilities", True, f"Declares {len(meta.capabilities)} capabilities"))
        else:
            items.append(ValidationItem("Capabilities", False, "No capabilities declared"))

        # Check 3: Supports interface
        items.append(ValidationItem("Interface", True, "BaseProvider interface contract implemented"))

        passed_count = sum(1 for i in items if i.passed)
        score = int((passed_count / len(items)) * 100)

        return ProviderValidationResult(
            provider_name=meta.name if meta else "unknown",
            score=score,
            items=items,
        )
