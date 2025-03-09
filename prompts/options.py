from dataclasses import dataclass
from enum import Enum


class OutputFormat(Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class JSONFormat(Enum):
    COMPACT = "compact"  # Original format with content as single string
    SPLIT = "split"      # New format with content split into lines


@dataclass
class Options:
    no_mask: bool = False
    output_file: str = "ppg_created_all.md.txt"
    output_format: OutputFormat = OutputFormat.JSON
    json_output_file: str = "project_data.json"
    json_format: JSONFormat = JSONFormat.SPLIT
