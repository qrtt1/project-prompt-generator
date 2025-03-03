"""
File processor module for handling file operations.
Contains functionality for reading files and applying language highlighting.
"""

import os
from typing import List

import pathspec

from .ignore_handler import load_gitignore_patterns
from .language_mapping import EXTENSION_MAPPING
from .types import FileEntry


def get_files_to_process(project_root, output_dir, output_file="ppg_created_all.md.txt"):
    """
    Get list of files to process, respecting .gitignore

    Args:
        project_root: Root directory of the project
        output_dir: Directory to exclude from processing
        output_file: All-in-one output file to exclude from processing

    Returns:
        List of file paths to process
    """
    # Load .gitignore patterns from multiple sources
    ignore_spec = load_gitignore_patterns(project_root)

    # Additional custom ignore patterns for directories
    default_ignore_dirs = {'promg.egg-info', 'venv', 'env', 'build', 'dist', '.pytest_cache'}
    custom_ignore_dirs_str = os.environ.get("CUSTOM_IGNORE_DIRS")
    if custom_ignore_dirs_str:
        custom_ignore_dirs = set(custom_ignore_dirs_str.split(','))
        custom_ignore_dirs.update(default_ignore_dirs)
    else:
        custom_ignore_dirs = default_ignore_dirs

    # Walk through the project directory and gather files
    files_to_process = []
    for root, dirs, files in os.walk(project_root):
        rel_root = os.path.relpath(root, project_root)
        # Skip the output directory
        if rel_root.startswith(output_dir):
            continue
        # Remove directories that you don't want to traverse
        dirs[:] = [d for d in dirs if d not in custom_ignore_dirs and d != ".git"]
        for file in files:
            file_full_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_full_path, project_root)

            # Skip files ignored by .gitignore
            if ignore_spec and ignore_spec.match_file(rel_path):
                continue

            # Skip the all-in-one output file
            if file == output_file:
                continue

            files_to_process.append(file_full_path)

    # Sort files for a consistent sequence order
    return sorted(files_to_process, key=lambda p: os.path.relpath(p, project_root))


def process_file(file_full_path, project_root, masker, no_mask, output_formatter):
    """
    Process a single file and generate its markdown representation

    Args:
        file_full_path: Path to the file to process
        project_root: Root directory of the project
        masker: SensitiveMasker instance
        no_mask: Flag to disable masking
        output_formatter: OutputFormatter instance

    Returns:
        Content as a string, or None if processing failed
    """
    rel_path = os.path.relpath(file_full_path, project_root)

    try:
        with open(file_full_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        print(f"Skipping {rel_path}: {e}")
        return None

    # Mask sensitive data by default unless disabled
    if masker and not no_mask:
        file_content = masker.mask_content(file_content)

    return file_content
