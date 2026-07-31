from hem.builders.plan_manager import PlanManager
from hem.generators.dashboard import DashboardGenerator
from hem.runtime.build_context import BuildContext


def test_dashboard_generator():
    ctx = BuildContext()
    gen = DashboardGenerator()
    model = gen.build_model(ctx)

    assert model.title == "HEM Dashboard"
    assert len(model.views) == 1
    assert len(model.views[0].cards) == 2


def test_plan_manager():
    pm = PlanManager()
    diff = pm.plan()

    assert len(diff.new_assets) > 0
    assert len(diff.new_entities) > 0
    assert len(diff.new_files) > 0
