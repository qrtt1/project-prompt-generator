"""
File processor module for handling file operations.
Contains functionality for reading files, applying language highlighting,
and creating markdown representations.
"""

import os
import pathspec

# Mapping file extensions to markdown language hints
EXTENSION_MAPPING = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    '.sh': 'bash',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.rb': 'ruby',
    '.php': 'php',
    '.go': 'go'
}


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
    # Load .gitignore patterns if the file exists
    gitignore_path = os.path.join(project_root, ".gitignore")
    ignore_spec = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            gitignore_lines = f.read().splitlines()
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_lines)

    # Additional custom ignore patterns for directories
    custom_ignore_dirs = {'promg.egg-info', 'venv', 'env', 'build', 'dist', '.pytest_cache'}

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
        print(f"Skipping {rel_path}: {e}")
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
