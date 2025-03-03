"""
Markdown formatter for converting project files to markdown.
"""
import os
from ..language_mapping import EXTENSION_MAPPING
from .output_formatter import OutputFormatter


class MarkdownFormatter(OutputFormatter):
    name = "markdown"
    file_extension = "md"

    def format(self, content, filename, rel_path):
        """
        Format content as markdown.

        Args:
            content (str): The content to format.
            filename (str): The name of the file.
            rel_path (str): The relative path to the file.

        Returns:
            str: The formatted content.
        """
        _, ext = os.path.splitext(filename)
        lang = EXTENSION_MAPPING.get(ext.lower(), '')
        code_block_start = f"```{lang}\n" if lang else "```\n"

        markdown_content = (
            "## file description\n\n"
            f"filename: {filename}\n"
            f"path: {rel_path}\n\n"
            "## content\n\n"
            f"{code_block_start}"
            f"{content}\n"
            "```"
        )
        return markdown_content

    def create_outline(self, files_info):
        """
        Create outline content from file info

        Args:
            files_info: List of FileEntry objects with file information

        Returns:
            Outline content as a string
        """
        outline_lines = ["# Outline\n"]
        for entry in files_info:
            outline_lines.append(
                f"- {entry.md_filename} (original: {entry.filename}, path: {entry.relative_path})")
        return "\n".join(outline_lines)
