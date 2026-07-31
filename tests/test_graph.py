from hem.builders.graph_manager import GraphManager
from hem.builders.build_manager import BuildManager


def test_graph_manager():
    ctx = BuildManager().build()
    gm = GraphManager()
    code = gm.generate_mermaid(ctx)

    assert "graph TD" in code
    assert "subgraph Assets" in code
    assert "subgraph Providers" in code
    assert "subgraph Generated Entities" in code
    assert "asset_brume" in code
