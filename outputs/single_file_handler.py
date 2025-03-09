import os
from os.path import expanduser

from utils.language_mapping import EXTENSION_MAPPING

from .events import Event
from .output_handler import OutputHandler


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

        lang = EXTENSION_MAPPING.get(ext, "")
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

    def _handle_outline_created(self, event):
        self.content += "# All Markdown Content\n\n"
        self.content += "## Outline\n\n"
        self.content += event.content + "\n\n"

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "rel_path": event.relative_path,
            "content": event.content,
            "ext": os.path.splitext(event.filename)[1].lower(),  # Extract extension
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
