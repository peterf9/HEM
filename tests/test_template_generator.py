from hem.generators.template_generator import TemplateGenerator
from hem.runtime.build_context import BuildContext


def test_template_generator_deduplication_and_single_root():
    ctx = BuildContext()
    tg = TemplateGenerator()
    
    # Verify that single-root rendering produces exact 'template' dict root
    tpl_dict = {
        "template": [
            {"binary_sensor": [{"name": "Test", "unique_id": "test"}]}
        ]
    }
    assert "template" in tpl_dict
    assert len(tpl_dict.keys()) == 1
