import os
from typing import Optional, Union

import pathspec


def build_ignores(project_root):
    """
    Loads gitignore patterns from multiple sources:
    1. .gitignore in the current working directory
    2. Files specified in the PPG_IGNORE_FILES environment variable

    Args:
        project_root (str): The root directory of the project.

    Returns:
        pathspec.PathSpec: A PathSpec object containing all gitignore patterns.
                           Returns None if no gitignore files are found.
    """
    patterns = ['.git', 'ppg_generated', 'ppg_created_all.md.txt']

    # Load .gitignore from current working directory if it exists
    gitignore_path = os.path.join(project_root, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            patterns.extend(f.read().splitlines())
        print(f"Loaded gitignore patterns from: {gitignore_path}")

    # Load gitignore files specified in PPG_IGNORE_FILES
    ignore_files_str = os.environ.get("PPG_IGNORE_FILES")
    if ignore_files_str:
        ignore_files = ignore_files_str.split(",")
        for ignore_file in ignore_files:
            ignore_file = ignore_file.strip()  # Remove leading/trailing whitespace
            if os.path.exists(ignore_file):
                with open(ignore_file, "r", encoding="utf-8") as f:
                    patterns.extend(f.read().splitlines())
                print(f"Loaded gitignore patterns from: {ignore_file}")
            else:
                print(f"Warning: gitignore file not found: {ignore_file}")

    if patterns:
        # Remove empty lines and strip whitespace
        patterns = [p.strip() for p in patterns if p.strip()]
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    else:
        return None
