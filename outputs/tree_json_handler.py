import json
import os
from os.path import expanduser

from outputs.events import Event
from utils.language_mapping import EXTENSION_MAPPING

from .output_handler import OutputHandler


class TreeJSONOutputHandler(OutputHandler):
    """
    Output handler for writing content in a tree-structured JSON format.
    The output mimics a filesystem tree with nested directories and files.
    """

    def __init__(self, output_file):
        """
        Initialize the output handler.

        Args:
            output_file (str): The path to the output file.
        """
        super().__init__()
        self.output_file = output_file
        self.file_tree = {"name": "root", "type": "directory", "children": {}}
        self.on("FileProcessedEvent", self._handle_file_processed)
        self.on("EndEvent", self._handle_end_event)

    def _handle_file_processed(self, event):
        """
        Handle a file processed event by adding it to the tree structure.

        Args:
            event: The FileProcessedEvent containing the processed file information
        """
        rel_path = event.relative_path
        parts = rel_path.split("/") if "/" in rel_path else rel_path.split("\\")
        filename = parts[-1]
        dirs = parts[:-1]

        # Navigate the tree structure and create directories as needed
        current = self.file_tree
        for dir_name in dirs:
            if dir_name not in current["children"]:
                current["children"][dir_name] = {
                    "name": dir_name,
                    "type": "directory",
                    "children": {}
                }
            current = current["children"][dir_name]

        # Add file to the current directory
        extension = os.path.splitext(filename)[1].lower()
        language = EXTENSION_MAPPING.get(extension, "")

        # Split content into lines
        content_lines = event.content.splitlines()

        current["children"][filename] = {
            "name": filename,
            "type": "file",
            "extension": extension,
            "language": language,
            "content": content_lines
        }

    def _convert_children_to_list(self, node):
        """
        Convert the children dictionary to a sorted list.

        Args:
            node: The node to process
        """
        if "children" in node and isinstance(node["children"], dict):
            # Sort directories first, then files
            dirs = []
            files = []

            for name, child in node["children"].items():
                if child["type"] == "directory":
                    self._convert_children_to_list(child)  # Process nested directories
                    dirs.append(child)
                else:
                    files.append(child)

            # Sort by name
            dirs.sort(key=lambda x: x["name"])
            files.sort(key=lambda x: x["name"])

            # Replace dictionary with sorted list
            node["children"] = dirs + files

    def _handle_end_event(self, event):
        """
        Handle the EndEvent by writing the tree structure to a JSON file.

        Args:
            event: The EndEvent containing the completion message
        """
        # Convert children dictionaries to sorted lists
        self._convert_children_to_list(self.file_tree)

        # Write tree structure to file
        with open(expanduser(self.output_file), "w", encoding="utf-8") as f:
            json.dump(self.file_tree, f, indent=2, ensure_ascii=False)
        print(f"Tree JSON output written to {self.output_file}")
        self.copy_to_clipboard(os.path.abspath(expanduser(self.output_file)))

    def fire_event(self, event: Event):
        """
        Fire an event to notify listeners.
        """
        event_name = type(event).__name__
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(event)
