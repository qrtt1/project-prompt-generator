import os
from typing import Optional, Union

import pathspec


def build_ignores(project_root):
    """
    Loads gitignore patterns from multiple sources:
    1. All .gitignore files from current directory up to git root
    2. Files specified in the PPG_IGNORE_FILES environment variable
    3. .git/info/exclude from the git repository root

    Args:
        project_root (str): The starting directory (usually current working directory).

    Returns:
        pathspec.PathSpec: A PathSpec object containing all gitignore patterns.
                           Returns None if no gitignore files are found.
    """
    patterns = ['.git', 'ppg_generated', 'ppg_created_all.md.txt']

    # Find git root directory (if we're in a git repo)
    git_root = None
    current_path = os.path.abspath(project_root)
    while current_path != os.path.dirname(current_path):  # Stop at filesystem root
        if os.path.exists(os.path.join(current_path, ".git")):
            git_root = current_path
            break
        current_path = os.path.dirname(current_path)

    # If we found a git root, collect all .gitignore files from current directory up to git root
    if git_root:
        # Find all .gitignore files from project_root up to git_root (closest first)
        current_path = os.path.abspath(project_root)
        gitignore_files = []
        
        while current_path != os.path.dirname(current_path) and current_path.startswith(git_root):
            gitignore_path = os.path.join(current_path, ".gitignore")
            if os.path.isfile(gitignore_path):
                gitignore_files.append(gitignore_path)
                print(f"Found .gitignore at: {gitignore_path}")
            current_path = os.path.dirname(current_path)

        # Process gitignore files in reverse order (git root first, then down to current dir)
        # This matches git's behavior where closer .gitignore files override parent ones
        for gitignore_path in reversed(gitignore_files):
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    file_patterns = f.read().splitlines()
                    # Add patterns with their directory context
                    rel_dir = os.path.relpath(os.path.dirname(gitignore_path), project_root)
                    if rel_dir == ".":
                        # Root .gitignore applies patterns as-is
                        patterns.extend(file_patterns)
                    else:
                        # Adjust patterns from subdirectories for proper matching
                        # (pathspec handles this internally)
                        patterns.extend(file_patterns)
                print(f"Loaded gitignore patterns from: {gitignore_path}")
            except Exception as e:
                print(f"Warning: Could not read {gitignore_path}: {e}")

        # Load .git/info/exclude if we found a git root
        git_exclude_path = os.path.join(git_root, ".git", "info", "exclude")
        if os.path.exists(git_exclude_path):
            try:
                with open(git_exclude_path, "r", encoding="utf-8") as f:
                    patterns.extend(f.read().splitlines())
                print(f"Loaded gitignore patterns from: {git_exclude_path}")
            except Exception as e:
                print(f"Warning: Could not read {git_exclude_path}: {e}")

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
        # Remove comment lines
        patterns = [p for p in patterns if not p.startswith('#')]
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    else:
        return None
