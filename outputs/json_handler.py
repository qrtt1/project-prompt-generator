import json
import os
from os.path import expanduser

from outputs.events import Event
from prompts.options import JSONFormat
from utils.language_mapping import EXTENSION_MAPPING

from .output_handler import OutputHandler


class JSONOutputHandler(OutputHandler):
    """
    Output handler for writing content in JSON format.
    Supports two formats:
    - compact: Original format with content as single string
    - split: New format with content split into lines
    """

    def __init__(self, output_file, json_format=JSONFormat.COMPACT):
        """
        Initialize the output handler.

        Args:
            output_file (str): The path to the output file.
            json_format (JSONFormat): The format to use for JSON output.
        """
        super().__init__()
        self.output_file = output_file
        self.json_format = json_format
        self.project_data = {"outline": [], "files": []}
        self.on("OutlineCreatedEvent", self._handle_outline_created)
        self.on("FileProcessedEvent", self._handle_file_processed)

    def _handle_outline_created(self, event):
        # Parse the outline content to create structured data
        outline_lines = event.content.split("\n")
        for line in outline_lines[2:]:  # Skip the "# Outline" header
            if line.strip().startswith("-"):
                # Extract information from the outline line
                parts = line.strip("- ").split(" (original: ")
                if len(parts) == 2:
                    md_filename = parts[0]
                    rest = parts[1].split(", path: ")
                    if len(rest) == 2:
                        original = rest[0]
                        path = rest[1].rstrip(")")
                        self.project_data["outline"].append(
                            {
                                "markdown_filename": md_filename,
                                "original_filename": original,
                                "path": path,
                            }
                        )

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "relative_path": event.relative_path,
            "extension": os.path.splitext(event.filename)[1].lower(),
            "language": EXTENSION_MAPPING.get(
                os.path.splitext(event.filename)[1].lower(), ""
            ),
        }

        # Handle content based on JSON format
        if self.json_format == JSONFormat.SPLIT:
            # Create content_lines with line numbers
            content_lines = []
            for i, line in enumerate(event.content.splitlines()):
                content_lines.append({"line_number": i + 1, "content": line})
            file_data["content_lines"] = content_lines
        else:  # COMPACT format
            file_data["content"] = event.content

        self.project_data["files"].append(file_data)

    def fire_event(self, event: Event):
        """
        Fire an event to notify listeners.
        """
        event_name = type(event).__name__
        if event_name == "EndEvent":
            with open(expanduser(self.output_file), "w", encoding="utf-8") as f:
                json.dump(self.project_data, f, indent=2, ensure_ascii=False)
        else:
            if event_name in self._event_handlers:
                for handler in self._event_handlers[event_name]:
                    handler(event)
