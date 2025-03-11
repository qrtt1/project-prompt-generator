from abc import ABC, abstractmethod
from typing import Callable

from outputs.events import Event


class OutputHandler(ABC):
    """
    Abstract base class for output handlers.
    """

    def __init__(self):
        self._event_handlers = {}

    def on(self, event_name: str, handler: Callable):
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def fire_event(self, event: Event):
        """
        Fire an event to notify listeners.
        """
        event_name = type(event).__name__
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(event)

    def copy_to_clipboard(self, output_file_path: str):
        from outputs import osx_copy_to_clipboard
        osx_copy_to_clipboard(output_file_path)
