"""
Base class for output formatters.
"""
import abc


class OutputFormatter(metaclass=abc.ABCMeta):
    name = "base"
    file_extension = "txt"

    @abc.abstractmethod
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

    @abc.abstractmethod
    def create_outline(self, files_info):
        """
        Create outline content from file info.

        Args:
            files_info (list): A list of FileEntry objects containing file info.

        Returns:
            str: The outline content.
        """
        raise NotImplementedError
