import os

from outputs.events import (EndEvent, FileProcessedEvent, OutlineCreatedEvent,
                            StartEvent)
from prompts import create_outline, process_file
from prompts.options import Options


def _create_masker(no_mask):
    """Create and configure the sensitive data masker"""
    from . import DEFAULT_SENSITIVE_PATTERNS, SensitiveMasker

    masker = None
    if not no_mask:
        # Initialize masker with default patterns if masking is enabled
        patterns = DEFAULT_SENSITIVE_PATTERNS.copy()
        masker = SensitiveMasker(patterns)

        if not no_mask:
            print("Sensitive data masking is enabled (use --no-mask to disable)")

    return masker


def generate(files_to_process, options: Options, output_handler):
    """
    Generate markdown output using the specified output handler.
    """
    masker = _create_masker(options.no_mask)

    output_handler.fire_event(StartEvent(message="Processing started"))

    try:
        markdown_files_info = []
        seq_counter = 1

        for file_entry in files_to_process:
            file_data = process_file(file_entry.full_path, os.getcwd(), masker, options.no_mask)
            if not file_data:
                continue

            # Generate reference filename (not creating actual file)
            flat_rel_path = file_entry.relative_path.replace(os.path.sep, "_")
            seq_str = str(seq_counter).zfill(3)
            md_filename = f"{seq_str}_{flat_rel_path}.md"

            markdown_files_info.append((seq_str, file_entry.filename, md_filename, file_entry.relative_path))

            event = FileProcessedEvent(filename=md_filename, relative_path=file_entry.relative_path,
                                       content=file_data["content"])
            output_handler.fire_event(event)
            print(f"Processed {file_entry.relative_path}")
            seq_counter += 1

        outline_content = create_outline(markdown_files_info)

        event = OutlineCreatedEvent(content=outline_content)
        output_handler.fire_event(event)

    finally:
        output_handler.fire_event(EndEvent(message="Processing completed"))
