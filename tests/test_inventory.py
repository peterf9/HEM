from hem.builders.build_manager import BuildManager
from hem.events.event_bus import EventBus
from hem.events.events import GeneratorFinishedEvent


def test_inventory_generator_and_events():
    events_received = []
    bus = EventBus()
    bus.subscribe(GeneratorFinishedEvent, lambda ev: events_received.append(ev.generator_name))

    manager = BuildManager(event_bus=bus)
    context = manager.build()

    assert context.inventory is not None
    assert len(context.inventory) > 0

    assert "InventoryGenerator" in events_received
    assert "ProviderGenerator" in events_received
    assert "ManifestGenerator" in events_received

    inventory_file = context.output_dir or (context.manifest.generated_files[0].parent / "inventory.json")
    assert inventory_file.exists()
