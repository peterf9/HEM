from hem.providers.catalog import ProviderCatalog
from hem.providers.ping import PingProvider
from hem.providers.validator import ProviderSDKValidator
from hem.runtime.build_context import BuildContext
from hem.runtime.execution_context import ExecutionContext


def test_execution_context():
    ctx = BuildContext()
    assert isinstance(ctx, ExecutionContext)
    assert ctx.version == "0.1.0"


def test_provider_catalog():
    cat = ProviderCatalog()
    all_entries = cat.list_all()
    assert len(all_entries) >= 5
    ping_search = cat.search("ping")
    assert len(ping_search) == 1
    assert ping_search[0].name == "ping"


def test_provider_sdk_validator():
    provider = PingProvider()
    validator = ProviderSDKValidator()
    result = validator.validate(provider)

    assert result.provider_name == "ping"
    assert result.score == 100
    assert all(item.passed for item in result.items)
