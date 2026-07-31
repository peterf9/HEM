from pathlib import Path
from hem.capabilities.availability import AvailabilityCapability
from hem.capabilities.bandwidth import NetworkBandwidthCapability
from hem.capabilities.cpu import CpuCapability
from hem.capabilities.memory import MemoryCapability
from hem.capabilities.storage import StorageCapability
from hem.capabilities.temperature import TemperatureCapability
from hem.contracts.asset import Asset
from hem.providers.base import BaseProvider
from hem.providers.metadata import ProviderMetadata
from hem.runtime.build_context import BuildContext
from hem.runtime.build_manifest import GeneratedEntity
from hem.runtime.paths import Paths


class InterfaceComponent:
    """SNMP Network Interface Component."""

    def __init__(self):
        self.bandwidth_capability = NetworkBandwidthCapability()

    def render(self, context: BuildContext, asset: Asset) -> str:
        return self.bandwidth_capability.render(context, asset)


class StorageComponent:
    """Storage Component."""

    def __init__(self):
        self.storage_capability = StorageCapability()

    def render(self, context: BuildContext, asset: Asset) -> str:
        return self.storage_capability.render(context, asset)


class EnvironmentComponent:
    """Environment Component (Temperature, Power, Fan)."""

    def __init__(self):
        self.temperature_capability = TemperatureCapability()

    def render(self, context: BuildContext, asset: Asset) -> str:
        return self.temperature_capability.render(context, asset)


class SnmpProvider(BaseProvider):

    def __init__(self):
        self.capabilities_map = {
            "availability": AvailabilityCapability(),
            "cpu": CpuCapability(),
            "memory": MemoryCapability(),
            "bandwidth": NetworkBandwidthCapability(),
            "storage": StorageCapability(),
            "temperature": TemperatureCapability(),
        }
        self.interface_component = InterfaceComponent()
        self.storage_component = StorageComponent()
        self.environment_component = EnvironmentComponent()

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="snmp",
            version="1.2.0",
            author="HEM Core",
            description="Production SNMP Monitoring Provider for Switches, Routers, Storage and Thermal Environment",
            capabilities=list(self.capabilities_map.keys()),
        )

    def supports(self, asset: Asset) -> bool:
        return asset.provider.lower() == "snmp"

    def generate(self, context: BuildContext, asset: Asset) -> None:
        templates_dir = Paths.templates()
        output_file = context.output_dir / "templates.yaml" if context.output_dir else Paths.hem_package_output() / "templates.yaml"

        rendered_sections = [f"\n# --- SNMP Provider Artifacts for {asset.name} ({asset.id}) ---"]

        for cap_name, capability in self.capabilities_map.items():
            rendered_code = capability.render(context, asset)
            rendered_sections.append(rendered_code)

            if context.manifest:
                context.manifest.generated_entities.append(
                    GeneratedEntity(
                        entity_id=f"{capability.platform}.hem_{asset.id}_{cap_name}",
                        platform=capability.platform,
                        generator=self.__class__.__name__,
                    )
                )

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:
            f.write("\n".join(rendered_sections) + "\n")

        if context.manifest and output_file not in context.manifest.generated_files:
            context.manifest.generated_files.append(output_file)

        context.statistics.files_generated = len(context.manifest.generated_files) if context.manifest else 1
        context.statistics.entities_generated += len(self.capabilities_map)
