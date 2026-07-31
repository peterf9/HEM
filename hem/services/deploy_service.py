import shutil
from pathlib import Path
from rich.console import Console

from hem.runtime.build_context import BuildContext
from hem.runtime.paths import Paths

console = Console()


class DeployService:

    def deploy(self, context: BuildContext, target_dir: Path) -> list[Path]:
        deployed_files = []

        if not context.manifest or not context.manifest.generated_files:
            return deployed_files

        target_dir.mkdir(parents=True, exist_ok=True)

        backup_dir = target_dir / ".backup"
        if target_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)

        for src_file in context.manifest.generated_files:
            if src_file.exists():
                dest_file = target_dir / src_file.name
                if dest_file.exists():
                    shutil.copy2(dest_file, backup_dir / dest_file.name)
                shutil.copy2(src_file, dest_file)
                deployed_files.append(dest_file)

        return deployed_files
