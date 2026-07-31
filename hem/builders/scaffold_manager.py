from pathlib import Path
from rich.console import Console

from hem.runtime.paths import Paths

console = Console()


class ScaffoldManager:

    def create_provider_scaffold(self, name: str) -> Path:
        name_clean = name.lower().strip()
        provider_dir = Paths.project_root() / "hem" / "providers" / name_clean
        provider_dir.mkdir(parents=True, exist_ok=True)
        templates_dir = provider_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        tests_dir = provider_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        init_file = provider_dir / "__init__.py"
        init_file.write_text(f'"""{name_clean.capitalize()} provider package."""\n', encoding="utf-8")

        provider_file = provider_dir / "provider.py"
        provider_file.write_text(f"""from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext


class {name_clean.capitalize()}Provider(BaseProvider):

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="{name_clean}",
            version="0.1.0",
            author="Community",
            description="{name_clean.capitalize()} monitoring provider scaffold",
            capabilities=["availability"],
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "{name_clean}"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        pass
""", encoding="utf-8")

        readme_file = provider_dir / "README.md"
        readme_file.write_text(f"# {name_clean.capitalize()} Provider\n\nScaffolded provider extension for HEM.\n", encoding="utf-8")

        return provider_dir
