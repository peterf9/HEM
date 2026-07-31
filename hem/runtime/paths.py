from pathlib import Path


class Paths:

    @staticmethod
    def project_root() -> Path:
        return Path.cwd()

    @staticmethod
    def assets() -> Path:
        return Paths.project_root() / "src" / "assets"

    @staticmethod
    def output() -> Path:
        return Paths.project_root() / "output"
