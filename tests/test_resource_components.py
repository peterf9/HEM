from hem.capabilities.storage import StorageCapability
from hem.capabilities.temperature import TemperatureCapability


def test_storage_temperature_capabilities():
    stg = StorageCapability()
    temp = TemperatureCapability()

    assert stg.metadata.name == "storage"
    assert stg.metadata.unit == "%"
    assert stg.metadata.icon == "mdi:harddisk"

    assert temp.metadata.name == "temperature"
    assert temp.metadata.unit == "°C"
    assert temp.metadata.device_class == "temperature"
