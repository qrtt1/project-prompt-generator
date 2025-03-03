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

    def create_outline(self, markdown_files_info):
        """
        Create outline content from file info.

        Args:
            markdown_files_info (list): A list of tuples containing file info.

        Returns:
            str: The outline content.
        """
        outline_content = "## Outline\n\n"
        for seq, filename, md_filename, rel_path in markdown_files_info:
            outline_content += f"{seq}. [{filename}]({md_filename}) - {rel_path}\n"
        return outline_content
