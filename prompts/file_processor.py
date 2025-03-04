"""
File processor module for handling file operations.
Contains functionality for reading files and masking data.
"""

import os


def process_file(file_full_path, project_root, masker, no_mask):
    """
    Process a single file and return its content and metadata.

    Args:
        file_full_path: Path to the file to process
        project_root: Root directory of the project
        masker: SensitiveMasker instance
        no_mask: Flag to disable masking

    Returns:
        A dictionary containing file content, relative path, and file extension,
        or None if processing failed.
    """
    rel_path = os.path.relpath(file_full_path, project_root)
    filename = os.path.basename(file_full_path)

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
    ext = ext.lower()

    return {
        "content": file_content,
        "rel_path": rel_path,
        "filename": filename,
        "ext": ext
    }


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
