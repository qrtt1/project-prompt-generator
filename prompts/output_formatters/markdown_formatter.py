"""
Markdown formatter for converting project files to markdown.
"""
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
        markdown_content = (
            "## file description\n\n"
            f"filename: {filename}\n"
            f"path: {rel_path}\n\n"
            "## contenxt\n\n"
        )
        markdown_content += content
        return markdown_content
