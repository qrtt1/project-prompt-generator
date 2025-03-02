"""
Configuration handler module for managing environment variables.
"""

import os
import re


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
