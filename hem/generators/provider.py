from pathlib import Path

from hem.generators.base import BaseGenerator


class ProviderGenerator(BaseGenerator):

    def generate(self, assets, output: Path):

        template = self.env.get_template("provider.j2")

        rendered = template.render(
            assets=assets
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output.write_text(
            rendered,
            encoding="utf-8"
        )
