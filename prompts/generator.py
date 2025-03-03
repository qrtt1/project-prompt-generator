"""
Generator module for converting project files.
Contains functionality for generating individual files and combined output.
"""

import os
import re
import shutil
from dataclasses import dataclass
from typing import List

from .config_handler import expand_path_variables
from .file_processor import create_outline, get_files_to_process, process_file
from .file_utils import ensure_directory_exists
from .sensitive_masker import DEFAULT_SENSITIVE_PATTERNS, SensitiveMasker
from .types import FileEntry
from .output_formatters import get_output_formatter  # Import the function instead

# Constants with environment variable overrides
# Expand both ~ and environment variables in paths
raw_output_dir = os.environ.get("PPG_OUTPUT_DIR", "ppg_generated")
raw_output_file = os.environ.get("PPG_OUTPUT_FILE", "ppg_created_all.md.txt")

OUTPUT_DIR = expand_path_variables(raw_output_dir)
SINGLE_OUTPUT_FILE = expand_path_variables(raw_output_file)


def _create_masker(no_mask):
    """Create and configure the sensitive data masker"""
    masker = None
    if not no_mask:
        # Initialize masker with default patterns if masking is enabled
        patterns = DEFAULT_SENSITIVE_PATTERNS.copy()
        masker = SensitiveMasker(patterns)

        if not no_mask:
            print("Sensitive data masking is enabled (use --no-mask to disable)")

    return masker


def collect_file_entries(project_root: str, files_to_process: List[str]) -> List[FileEntry]:
    """
    Collects file information into a list of FileEntry objects.
    """
    file_list: List[FileEntry] = []
    seq_counter = 1
    for file_path in files_to_process:
        rel_path = os.path.relpath(file_path, project_root)
        file_list.append(
            FileEntry(
                sequence=seq_counter,
                relative_path=rel_path,
                filename=os.path.basename(file_path),  # Just the filename
                file_full_path=file_path,
            )
        )
        seq_counter += 1
    return file_list


def process_and_format_file(
    file_entry: FileEntry,
    project_root: str,
    masker,
    no_mask: bool,
    output_formatter,  # Remove type hint
    output_dir_path: str,
) -> None:
    """
    Processes a single file, formats the content, and writes it to the output directory.
    """
    processed_content = process_file(
        file_entry.file_full_path, project_root, masker, no_mask
    )
    if not processed_content:
        print(f"Skipping {file_entry.relative_path} due to processing error.")
        return

    # Generate a flat version of the relative path
    flat_rel_path = file_entry.relative_path.replace(os.path.sep, "_")
    seq_str = str(file_entry.sequence).zfill(3)
    md_filename = f"{seq_str}_{flat_rel_path}.{output_formatter.file_extension}"
    md_filepath = os.path.join(output_dir_path, md_filename)

    formatted_content = output_formatter.format(
        processed_content,
        file_entry.filename,  # Use filename from FileEntry
        file_entry.relative_path,
    )

    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(formatted_content)

    print(
        f"Converted {file_entry.relative_path} to {output_formatter.name} as {md_filename}"
    )


def generate_individual_files(no_mask, output_formatter):
    """Generate individual files in the output directory"""
    # Define the project root as the current working directory
    project_root = os.getcwd()

    # Remove the output directory if it exists and recreate it
    output_dir_path = os.path.join(project_root, OUTPUT_DIR)
    # Handle absolute paths if OUTPUT_DIR is absolute
    if os.path.isabs(OUTPUT_DIR):
        output_dir_path = OUTPUT_DIR

    if os.path.exists(output_dir_path):
        shutil.rmtree(output_dir_path)
    os.makedirs(output_dir_path)

    # Get files and initialize masker
    files_to_process = get_files_to_process(project_root, OUTPUT_DIR, SINGLE_OUTPUT_FILE)
    masker = _create_masker(no_mask)

    file_list = collect_file_entries(project_root, files_to_process)

    # Process each file
    for file_entry in file_list:
        process_and_format_file(file_entry, project_root, masker, no_mask, output_formatter, output_dir_path)


    # Create outline file
    outline_content = create_outline(file_list)
    outline_filename = f"000_outline.{output_formatter.file_extension}"
    outline_path = os.path.join(output_dir_path, outline_filename)

    formatted_outline = output_formatter.format(outline_content, "000_outline", "")

    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(formatted_outline)

    print(f"Outline file created as {outline_filename}")
    print(f"Generated {len(file_list)} individual files in {OUTPUT_DIR}/")


def generate_single_file(no_mask, output_formatter):
    """Generate a single file with all content"""
    project_root = os.getcwd()

    # Get files and initialize masker
    files_to_process = get_files_to_process(project_root, OUTPUT_DIR, SINGLE_OUTPUT_FILE)
    masker = _create_masker(no_mask)

    file_list: List[FileEntry] = []
    seq_counter = 1

    # Process each file
    for file_full_path in files_to_process:
        rel_path = os.path.relpath(file_full_path, project_root)
        processed_content = process_file(file_full_path, project_root, masker, no_mask)
        if not processed_content:
            continue

        # Generate reference filename (not creating actual file)
        flat_rel_path = rel_path.replace(os.path.sep, "_")
        file_list.append(FileEntry(sequence=seq_counter, relative_path=rel_path, filename=file_full_path,
                                   file_full_path=file_full_path))
        print(f"Processed {rel_path}")
        seq_counter += 1

    # Create the outline
    outline_content = create_outline(file_list)

    # Create the all-in-one file
    all_file_path = SINGLE_OUTPUT_FILE
    if not os.path.isabs(SINGLE_OUTPUT_FILE):
        all_file_path = os.path.join(project_root, SINGLE_OUTPUT_FILE)

    # Ensure parent directory exists
    ensure_directory_exists(all_file_path)

    with open(all_file_path, "w", encoding="utf-8") as f_all:
        f_all.write(f"# All Content\n\n")
        f_all.write(f"## Outline\n\n")

        formatted_outline = output_formatter.format(outline_content, "Outline", "")
        f_all.write(formatted_outline)
        f_all.write("\n\n")

        # Write content for each file
        for entry in file_list:
            file_path = os.path.join(project_root, entry.relative_path)
            processed_content = process_file(entry.file_full_path, project_root, masker, no_mask)
            if not processed_content:
                continue

            file_header = f"---{output_formatter.file_extension}\n## {entry.md_filename} (from {entry.relative_path})\n\n"
            f_all.write(file_header)

            formatted_content = output_formatter.format(processed_content, os.path.basename(file_path),
                                                        entry.relative_path)
            f_all.write(formatted_content)
            f_all.write("\n\n")

    print(f"Created single all-in-one file: {all_file_path}")
