"""
Prompts package for project-prompt-generator.
Contains modules for generating markdown files from project files.
"""

from .file_processor import create_outline, process_file
from .generator import generate
from .sensitive_masker import (DEFAULT_SENSITIVE_PATTERNS, SensitiveMasker,
                               mask_sensitive_data)

__all__ = [
    'SensitiveMasker',
    'mask_sensitive_data',
    'DEFAULT_SENSITIVE_PATTERNS',
    'process_file',
    'create_outline',
    'generate',
]
