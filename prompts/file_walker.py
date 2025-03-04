"""
File walker module for handling file system traversal and filtering.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import pathspec


@dataclass
class FileEntry:
    """
    Data class to represent a file entry with its full path, relative path, and filename.
    """
    full_path: str
    relative_path: str
    filename: str

    @property
    def flattened_relative_path(self):
        """
        Returns a flattened version of the relative path with underscores instead of path separators
        and without the .md extension.
        """
        return self.relative_path.replace(os.path.sep, "_").replace(Path(self.relative_path).suffix, "")


class FileWalker:
    """
    Encapsulates the logic for walking a directory and collecting files.
    """

    def __init__(self, project_root: Union[str, os.PathLike], ignore_spec: Optional[pathspec.PathSpec] = None):
        """
        Initializes the FileWalker with the project root.

        Args:
            project_root (str): The root directory of the project.
            ignore_spec (pathspec.PathSpec, optional): A PathSpec object containing gitignore patterns. Defaults to None.
        """
        self.project_root = project_root
        self.ignore_spec = ignore_spec

    def get_files(self):
        """
        Walks the project directory and returns a list of FileEntry objects,
        respecting the provided ignore patterns.

        Returns:
            list: A sorted list of FileEntry objects.
        """
        file_entries = []
        for root, dirs, filenames in os.walk(self.project_root):
            # Modify dirs in-place to prevent walking ignored directories
            if self.ignore_spec:
                new_dirs = []
                for d in dirs:
                    full_dir_path = os.path.join(root, d)
                    relative_dir_path = os.path.relpath(full_dir_path, self.project_root)
                    if self.ignore_spec.match_file(relative_dir_path):
                        pass
                    else:
                        new_dirs.append(d)
                dirs[:] = new_dirs

            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, self.project_root)

                # Apply ignorance rules
                if self.ignore_spec and self.ignore_spec.match_file(relative_path):
                    continue  # Skip ignored files

                entry = FileEntry(full_path=full_path, relative_path=relative_path, filename=filename)
                file_entries.append(entry)
        return sorted(file_entries, key=lambda it: it.relative_path)


if __name__ == '__main__':
    # Example usage of the FileWalker class
    import prompts

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(prompts.__file__)))

    ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", ["*.txt", "venv"])
    walker = FileWalker(project_root, ignore_spec)
    files = walker.get_files()
    for file_entry in files:
        print(file_entry.relative_path)
        print(file_entry.filename)
        print(file_entry.flattened_relative_path)
        print()
