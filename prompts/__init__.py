"""
Prompts package for project-prompt-generator.
Contains modules for generating markdown files from project files.
"""

from .sensitive_masker import SensitiveMasker, mask_sensitive_data, DEFAULT_SENSITIVE_PATTERNS
from .file_processor import process_file, get_files_to_process, create_outline
from .generator import generate_individual_files, generate_single_file

__all__ = [
    'SensitiveMasker',
    'mask_sensitive_data',
    'DEFAULT_SENSITIVE_PATTERNS',
    'process_file',
    'get_files_to_process',
    'create_outline',
    'generate_individual_files',
    'generate_single_file'
]