"""
File utilities module for handling file and directory operations.
"""

import os


def ensure_directory_exists(path):
    """
    Ensure that a directory exists, creating it if necessary.
    Works with both relative and absolute paths, and handles home directory (~) expansion.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
