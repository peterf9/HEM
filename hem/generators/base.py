from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class BaseGenerator(ABC):

    def __init__(self, template_path: Path):

        self.env = Environment(
            loader=FileSystemLoader(template_path)
        )

    @abstractmethod
    def generate(self, *args, **kwargs):
        pass
