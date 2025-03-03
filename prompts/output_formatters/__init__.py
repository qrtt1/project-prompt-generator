from .markdown_formatter import MarkdownFormatter
from .json_formatter import JsonFormatter

def get_output_formatter(format_name: str):
    if format_name == "markdown":
        return MarkdownFormatter()
    elif format_name == "json":
        return JsonFormatter()
    else:
        raise ValueError(f"Unsupported output format: {format_name}")
