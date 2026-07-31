from hem.builders.build_manager import BuildManager


def test_build_manager():
    manager = BuildManager()
    context = manager.build()

    assert context.statistics.assets_loaded > 0
    assert context.statistics.assets_validated > 0
    assert context.statistics.files_generated >= 2
    assert context.manifest is not None
    assert len(context.manifest.generated_files) >= 2
    assert any(f.name == "templates.yaml" for f in context.manifest.generated_files)
    assert any(f.name == "manifest.json" for f in context.manifest.generated_files)
