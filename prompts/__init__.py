"""
Prompts package for project-prompt-generator.
Contains modules for generating markdown files from project files.
"""

from .file_processor import get_files_to_process, process_file
from .generator import generate_individual_files, generate_single_file
from .ignore_handler import load_gitignore_patterns
from .sensitive_masker import (DEFAULT_SENSITIVE_PATTERNS, SensitiveMasker,
                               mask_sensitive_data)

__all__ = [
    'SensitiveMasker',
    'mask_sensitive_data',
    'DEFAULT_SENSITIVE_PATTERNS',
    'process_file',
    'get_files_to_process',
    'generate_individual_files',
    'generate_single_file',
    'load_gitignore_patterns'
]
