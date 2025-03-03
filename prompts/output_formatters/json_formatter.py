import json

class JsonFormatter:
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
