from dataclasses import dataclass
from enum import Enum


class OutputFormat(Enum):
    MARKDOWN = "markdown"
    JSON = "json"


@dataclass
class Options:
    no_mask: bool = False
    output_dir: str = "ppg_generated"
    output_file: str = "ppg_created_all.md.txt"
    output_format: OutputFormat = OutputFormat.MARKDOWN
    json_output_file: str = "project_data.json"
