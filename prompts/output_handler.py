import os
import json
from abc import ABC, abstractmethod
from os.path import expanduser
from typing import Callable, Dict, List

from utils.language_mapping import EXTENSION_MAPPING
from .events import Event
from .options import JSONFormat


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

    def _create_markdown_content(self, file_data):
        """
        Create markdown representation from file data.

        Args:
            file_data (dict): Dictionary containing file content, relative path, filename, and extension.

        Returns:
            str: Markdown content as a string.
        """
        filename = file_data["filename"]
        rel_path = file_data["rel_path"]
        file_content = file_data["content"]
        ext = file_data["ext"]

        lang = EXTENSION_MAPPING.get(ext, '')
        code_block_start = f"```{lang}\n" if lang else "```\n"

        markdown_content = (
            "## file description\n\n"
            f"filename: {filename}\n"
            f"path: {rel_path}\n\n"
            "## contenxt\n\n"
            f"{code_block_start}"
            f"{file_content}\n"
            "```"
        )
        return markdown_content


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
        self.output_dir = expanduser(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self.on("FileProcessedEvent", self._handle_file_processed)

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "rel_path": event.relative_path,
            "content": event.content,
            "ext": os.path.splitext(event.filename)[1].lower()  # Extract extension
        }
        markdown_content = self._create_markdown_content(file_data)
        filepath = os.path.join(self.output_dir, event.filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)


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

    def _handle_outline_created(self, event):
        self.content += "# All Markdown Content\n\n"
        self.content += "## Outline\n\n"
        self.content += event.content + "\n\n"

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "rel_path": event.relative_path,
            "content": event.content,
            "ext": os.path.splitext(event.filename)[1].lower()  # Extract extension
        }
        markdown_content = self._create_markdown_content(file_data)
        self.content += f"---\n" + markdown_content + "\n\n"

    def fire_event(self, event: Event):
        """
        Fire an event to notify listeners.
        """
        event_name = type(event).__name__
        if event_name == "EndEvent":
            with open(expanduser(self.output_file), "w", encoding="utf-8") as f:
                f.write(self.content)
        else:
            if event_name in self._event_handlers:
                for handler in self._event_handlers[event_name]:
                    handler(event)


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
        self.project_data = {
            "outline": [],
            "files": []
        }
        self.on("OutlineCreatedEvent", self._handle_outline_created)
        self.on("FileProcessedEvent", self._handle_file_processed)

    def _handle_outline_created(self, event):
        # Parse the outline content to create structured data
        outline_lines = event.content.split('\n')
        for line in outline_lines[2:]:  # Skip the "# Outline" header
            if line.strip().startswith('-'):
                # Extract information from the outline line
                parts = line.strip('- ').split(' (original: ')
                if len(parts) == 2:
                    md_filename = parts[0]
                    rest = parts[1].split(', path: ')
                    if len(rest) == 2:
                        original = rest[0]
                        path = rest[1].rstrip(')')
                        self.project_data["outline"].append({
                            "markdown_filename": md_filename,
                            "original_filename": original,
                            "path": path
                        })

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "relative_path": event.relative_path,
            "extension": os.path.splitext(event.filename)[1].lower(),
            "language": EXTENSION_MAPPING.get(os.path.splitext(event.filename)[1].lower(), '')
        }

        # Handle content based on JSON format
        if self.json_format == JSONFormat.SPLIT:
            file_data["content_lines"] = event.content.splitlines()
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
