import json

from .output_formatter import OutputFormatter

class JsonFormatter(OutputFormatter):
    """
    JSON Formatter that converts prompt content along with file metadata into JSON format.
    """
    name = "json"
    file_extension = "json"

    def format(self, content: str, filename: str, file_path: str) -> str:
        """
        Formats the provided content, filename, and file_path into a JSON string.
        """
        output = {
            "content": content,
            "filename": filename,
            "file_path": file_path,
        }
        return json.dumps(output, ensure_ascii=False, indent=2)

    def generate_all_in_one(self, outputs: list) -> str:
        """
        Aggregates a list of output dictionaries into a single JSON string representing all outputs.
        Each dictionary in the list should have keys: 'content', 'filename', and 'file_path'.
        """
        aggregated = {
            "outputs": outputs
        }
        return json.dumps(aggregated, ensure_ascii=False, indent=2)

    def create_outline(self, files_info):
        """
        Create outline content from file info for JSON format.

        Args:
            files_info: List of FileEntry objects with file information

        Returns:
            Outline content as a JSON string
        """
        outline_data = []
        for entry in files_info:
            outline_data.append({
                "md_filename": entry.md_filename,
                "original": entry.filename,
                "path": entry.relative_path
            })
        return json.dumps(outline_data, ensure_ascii=False, indent=2)
