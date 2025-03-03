from .output_formatter import OutputFormatter
from .markdown_formatter import MarkdownFormatter

_formatters = {
    "markdown": MarkdownFormatter,
}


def get_output_formatter(format_name):
    formatter_class = _formatters.get(format_name.lower())
    if not formatter_class:
        raise ValueError(f"Unsupported output format: {format_name}")
    return formatter_class()
