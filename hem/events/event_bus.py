from typing import Callable, Dict, List

class EventBus:

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def emit(self, event_type: str, data: any = None) -> None:
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(data)
