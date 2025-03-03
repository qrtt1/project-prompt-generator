import os
from abc import ABC, abstractmethod
from os.path import expanduser
from typing import Callable

from .events import Event


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

    @abstractmethod
    def write(self, filename: str, relative_path: str, content: str):
        """
        Write content to the output.
        """
        pass


class IndividualFilesOutputHandler(OutputHandler):
    """
    Output handler for writing content to individual files.
    """

    def __init__(self, output_dir):
        """
        Initialize the output handler.

        Args:
            output_dir (str): The directory to write the files to.
        """
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.on("FileProcessedEvent", self._handle_file_processed)

    def write(self, filename: str, relative_path: str, content: str):
        """
        Write content to the file.

        Args:
            content (str): The content to write.
        """
        pass

    def _handle_file_processed(self, event):
        filename = event.filename
        content = event.content
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {filepath}")


class SingleFileOutputHandler(OutputHandler):
    """
    Output handler for writing content to a single file.
    """

    def __init__(self, output_file):
        """
        Initialize the output handler.

        Args:
            output_file (str): The path to the output file.
        """
        super().__init__()
        self.output_file = output_file
        self.content = ""
        self.on("OutlineCreatedEvent", self._handle_outline_created)
        self.on("FileProcessedEvent", self._handle_file_processed)

    def write(self, filename: str, relative_path: str, content: str):
        """
        Write content to the output file.

        Args:
            content (str): The content to write.
        """
        pass

    def _handle_outline_created(self, event):
        self.content += "# All Markdown Content\n\n"
        self.content += "## Outline\n\n"
        self.content += event.content + "\n\n"

    def _handle_file_processed(self, event):
        self.content += f"---\n## {event.filename} (from {event.relative_path})\n\n"
        self.content += event.content + "\n\n"

    def fire_event(self, event: Event):
        """
        Fire an event to notify listeners.
        """
        event_name = type(event).__name__
        if event_name == "EndEvent":
            with open(expanduser(self.output_file), "w", encoding="utf-8") as f:
                f.write(self.content)
            print(f"Created single all-in-one file: {self.output_file}")
        else:
            if event_name in self._event_handlers:
                for handler in self._event_handlers[event_name]:
                    handler(event)
