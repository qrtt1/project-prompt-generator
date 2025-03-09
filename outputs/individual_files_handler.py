import os
from os.path import expanduser

from outputs import OutputHandler
from utils.language_mapping import EXTENSION_MAPPING


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

    def _handle_file_processed(self, event):
        file_data = {
            "filename": event.filename,
            "rel_path": event.relative_path,
            "content": event.content,
            "ext": os.path.splitext(event.filename)[1].lower(),  # Extract extension
        }
        markdown_content = self._create_markdown_content(file_data)
        filepath = os.path.join(self.output_dir, event.filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
