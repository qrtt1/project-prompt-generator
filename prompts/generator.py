"""
Generator module for converting project files to markdown.
Contains functionality for generating individual markdown files and combined output.
"""

import os
import shutil
import pathspec
import re
from .sensitive_masker import SensitiveMasker, DEFAULT_SENSITIVE_PATTERNS
from .file_processor import process_file, get_files_to_process, create_outline

def expand_path_variables(path):
    """
    Expand environment variables in a path string.
    Handles both $VAR and ${VAR} formats, as well as ~ for home directory.
    """
    if not path:
        return path

    # First pass: expand ~ for home directory
    path = os.path.expanduser(path)

    # Second pass: handle ${VAR} format
    path = os.path.expandvars(path)

    # Third pass: handle $VAR format (for any remaining variables)
    # This is a fallback in case os.path.expandvars missed any
    def replace_var(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    path = re.sub(r'\$([A-Za-z0-9_]+)', replace_var, path)

    return path

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


def ensure_directory_exists(path):
    """
    Ensure that a directory exists, creating it if necessary.
    Works with both relative and absolute paths, and handles home directory (~) expansion.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def generate_individual_files(no_mask):
    """Generate individual markdown files in the output directory"""
    # Define the project root as the current working directory
    project_root = os.getcwd()

    # Log the output directory being used (helpful when using environment variables)
    print(f"Using output directory: {OUTPUT_DIR}")

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

    markdown_files_info = []
    seq_counter = 1

    # Process each file
    for file_full_path in files_to_process:
        rel_path = os.path.relpath(file_full_path, project_root)
        markdown_content = process_file(file_full_path, project_root, masker, no_mask)
        if not markdown_content:
            continue

        # Generate a flat version of the relative path
        flat_rel_path = rel_path.replace(os.path.sep, "_")

        seq_str = str(seq_counter).zfill(3)
        md_filename = f"{seq_str}_{flat_rel_path}.md"
        md_filepath = os.path.join(output_dir_path, md_filename)

        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        markdown_files_info.append((seq_str, os.path.basename(file_full_path), md_filename, rel_path))
        print(f"Converted {rel_path} to markdown as {md_filename}")
        seq_counter += 1

    # Create outline file
    outline_content = create_outline(markdown_files_info)
    outline_path = os.path.join(output_dir_path, "000_outline.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(outline_content)

    print("Outline file created as 000_outline.md")
    print(f"Generated {len(markdown_files_info)} individual markdown files in {OUTPUT_DIR}/")


def generate_single_file(no_mask):
    """Generate a single markdown file with all content"""
    project_root = os.getcwd()

    # Log the output file being used (helpful when using environment variables)
    print(f"Using output file: {SINGLE_OUTPUT_FILE}")

    # Get files and initialize masker
    files_to_process = get_files_to_process(project_root, OUTPUT_DIR, SINGLE_OUTPUT_FILE)
    masker = _create_masker(no_mask)

    markdown_files_info = []
    seq_counter = 1

    # Process each file
    for file_full_path in files_to_process:
        rel_path = os.path.relpath(file_full_path, project_root)
        markdown_content = process_file(file_full_path, project_root, masker, no_mask)
        if not markdown_content:
            continue

        # Generate reference filename (not creating actual file)
        flat_rel_path = rel_path.replace(os.path.sep, "_")
        seq_str = str(seq_counter).zfill(3)
        md_filename = f"{seq_str}_{flat_rel_path}.md"

        markdown_files_info.append((seq_str, os.path.basename(file_full_path), md_filename, rel_path))
        print(f"Processed {rel_path}")
        seq_counter += 1

    # Create the outline
    outline_content = create_outline(markdown_files_info)

    # Create the all-in-one file
    all_file_path = SINGLE_OUTPUT_FILE
    if not os.path.isabs(SINGLE_OUTPUT_FILE):
        all_file_path = os.path.join(project_root, SINGLE_OUTPUT_FILE)

    # Ensure parent directory exists
    ensure_directory_exists(all_file_path)

    with open(all_file_path, "w", encoding="utf-8") as f_all:
        f_all.write("# All Markdown Content\n\n")
        f_all.write("## Outline\n\n")
        f_all.write(outline_content)
        f_all.write("\n\n")

        # Write content for each file
        for seq, original, md_filename, rel_path in markdown_files_info:
            file_path = os.path.join(project_root, rel_path)
            markdown_content = process_file(file_path, project_root, masker, no_mask)
            if not markdown_content:
                continue

            f_all.write(f"---\n## {md_filename} (from {rel_path})\n\n")
            f_all.write(markdown_content)
            f_all.write("\n\n")

    print(f"Created single all-in-one file: {all_file_path}")
