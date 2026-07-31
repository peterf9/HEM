from hem.capabilities.cpu import CpuCapability
from hem.capabilities.memory import MemoryCapability
from hem.providers.snmp import SnmpProvider
from hem.runtime.build_context import BuildContext


def test_snmp_provider_production():
    provider = SnmpProvider()
    assert provider.metadata.name == "snmp"
    assert provider.metadata.version == "1.0.0"
    assert "cpu" in provider.metadata.capabilities
    assert "memory" in provider.metadata.capabilities


def test_cpu_memory_capabilities():
    cpu_cap = CpuCapability()
    mem_cap = MemoryCapability()

    assert cpu_cap.metadata.name == "cpu"
    assert cpu_cap.metadata.unit == "%"
    assert mem_cap.metadata.name == "memory"
    assert mem_cap.metadata.unit == "%"
