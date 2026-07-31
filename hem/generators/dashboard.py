import yaml
from hem.dashboards.model import DashboardCard, DashboardModel, DashboardView
from hem.generators.base import BaseGenerator
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class DashboardGenerator(BaseGenerator):

    def build_model(self, context: BuildContext) -> DashboardModel:
        cards = [
            DashboardCard(
                type="markdown",
                title="HEM System Status",
                content={
                    "content": f"### HEM Observability Framework\n- **Version**: {context.version}\n- **Assets**: {context.statistics.assets_loaded}\n- **Build Time**: {context.statistics.build_time_ms:.2f}ms"
                },
            ),
            DashboardCard(
                type="entities",
                title="Monitored Entities",
                content={
                    "entities": [
                        e.entity_id for e in (context.manifest.generated_entities if context.manifest else [])
                    ]
                },
            ),
        ]

        view = DashboardView(
            title="HEM Overview",
            path="hem_overview",
            icon="mdi:view-dashboard-outline",
            cards=cards,
        )

        return DashboardModel(title="HEM Dashboard", views=[view])

    def generate(self, context: BuildContext) -> None:
        model = self.build_model(context)

        lovelace_dict = {
            "title": model.title,
            "views": [
                {
                    "title": v.title,
                    "path": v.path,
                    "icon": v.icon,
                    "cards": [
                        {"type": c.type, "title": c.title, **c.content} for c in v.cards
                    ],
                }
                for v in model.views
            ],
        }

        rendered = yaml.dump(lovelace_dict, sort_keys=False)

        output_file = (context.output_dir or Paths.hem_package_output()) / "dashboards" / "hem_dashboard.yaml"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(rendered, encoding="utf-8")

        if context.manifest and output_file not in context.manifest.generated_files:
            context.manifest.generated_files.append(output_file)

        if context.manifest:
            context.manifest.generated_entities.append(
                GeneratedEntity(
                    entity_id="dashboard.hem_overview",
                    platform="lovelace",
                    generator="DashboardGenerator",
                )
            )

        context.statistics.files_generated = len(context.manifest.generated_files) if context.manifest else 1
        context.statistics.entities_generated += 1
