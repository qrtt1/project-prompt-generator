"""
File processor module for handling file operations.
Contains functionality for reading files, applying language highlighting,
and creating markdown representations.
"""

import os

from .language_mapping import EXTENSION_MAPPING


def process_file(file_full_path, project_root, masker, no_mask):
    """
    Process a single file and generate its markdown representation

    Args:
        file_full_path: Path to the file to process
        project_root: Root directory of the project
        masker: SensitiveMasker instance
        no_mask: Flag to disable masking

    Returns:
        Markdown content as a string, or None if processing failed
    """
    rel_path = os.path.relpath(file_full_path, project_root)

    try:
        with open(file_full_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        # print(f"Skipping {rel_path}: {e}")
        return None

    # Mask sensitive data by default unless disabled
    if masker and not no_mask:
        file_content = masker.mask_content(file_content)

    # Determine language hint based on file extension
    _, ext = os.path.splitext(file_full_path)
    lang = EXTENSION_MAPPING.get(ext.lower(), '')
    code_block_start = f"```{lang}\n" if lang else "```\n"

    # Create markdown representation
    markdown_content = (
        "## file description\n\n"
        f"filename: {os.path.basename(file_full_path)}\n"
        f"path: {rel_path}\n\n"
        "## contenxt\n\n"
        f"{code_block_start}"
        f"{file_content}\n"
        "```"
    )

    return markdown_content


def create_outline(markdown_files_info):
    """
    Create outline content from file info

    Args:
        markdown_files_info: List of tuples with file information

    Returns:
        Outline content as a string
    """
    outline_lines = ["# Outline\n"]
    for seq, original, md_filename, rel_path in markdown_files_info:
        outline_lines.append(f"- {md_filename} (original: {original}, path: {rel_path})")
    return "\n".join(outline_lines)
