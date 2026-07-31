import importlib
import pkgutil
from typing import Dict, List, Type

from hem.providers.base import BaseProvider


class ProviderRegistry:

    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        self._providers[provider.metadata.name] = provider

    def get(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    def providers(self) -> List[BaseProvider]:
        return list(self._providers.values())

    def discover(self) -> None:
        import hem.providers as providers_pkg
        for _, module_name, is_pkg in pkgutil.iter_modules(providers_pkg.__path__):
            if is_pkg:
                try:
                    module = importlib.import_module(f"hem.providers.{module_name}.provider")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, BaseProvider)
                            and attr is not BaseProvider
                        ):
                            instance = attr()
                            self.register(instance)
                except ModuleNotFoundError:
                    pass
