from dataclasses import dataclass


@dataclass
class Options:
    no_mask: bool = False
    output_dir: str = "ppg_generated"
    output_file: str = "ppg_created_all.md.txt"
