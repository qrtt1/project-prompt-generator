"""
Base class for output formatters.
"""
import abc


class OutputFormatter(metaclass=abc.ABCMeta):
    name = "base"
    file_extension = "txt"

    def format(self, content, filename, rel_path):
        """
        Format the content.

        Args:
            content (str): The content to format.
            filename (str): The name of the file.
            rel_path (str): The relative path to the file.

        Returns:
            str: The formatted content.
        """
        return content
