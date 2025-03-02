"""
Tests for the file_processor module, specifically the text replacement feature.
"""

import pytest
from prompts.file_processor import process_file
from prompts.sensitive_masker import SensitiveMasker
import os
import tempfile

# Mock masker for testing purposes
MASKER = SensitiveMasker()


@pytest.fixture(scope="function")
def temp_project_root():
    """
    Fixture to create a temporary project root directory.
    This will be cleaned up after each test function.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def create_dummy_file(project_root, filepath, content):
    """Creates a dummy file for testing within the temporary directory."""
    full_path = os.path.join(project_root, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path


def test_text_replacement(temp_project_root):
    # Create a dummy file with some content
    file_content = "This is a test file.\nReplace this word."
    filepath = create_dummy_file(temp_project_root, "test_file.txt", file_content)

    # Define replacements
    replace = {"test": "success", "word": "string"}

    # Process the file with replacements
    markdown_content = process_file(filepath, temp_project_root, MASKER, False, replace)

    # Assert that the replacements were made
    assert "This is a success file." in markdown_content
    assert "Replace this string." in markdown_content


def test_text_replacement_no_replace(temp_project_root):
    # Test when no replacements are provided
    file_content = "This is a test file."
    filepath = create_dummy_file(temp_project_root, "test_file.txt", file_content)

    # Process the file without replacements
    markdown_content = process_file(filepath, temp_project_root, MASKER, False)

    # Assert that the content remains unchanged
    assert "This is a test file." in markdown_content


def test_text_replacement_empty_file(temp_project_root):
    # Test with an empty file
    filepath = create_dummy_file(temp_project_root, "test_file.txt", "")

    # Define replacements (though they shouldn't have any effect)
    replace = {"test": "success"}

    # Process the empty file
    markdown_content = process_file(filepath, temp_project_root, MASKER, False, replace)

    # Assert that the markdown content for an empty file is still generated
    assert "## file description" in markdown_content
    assert "filename: test_file.txt" in markdown_content


def test_text_replacement_special_chars(temp_project_root):
    # Test replacement with special characters in old/new strings
    file_content = "Special chars: $, ^, *, +, ?, ., \\"
    filepath = create_dummy_file(temp_project_root, "test_file.txt", file_content)

    # Define replacements with special chars
    replace = {"$": "USD", "^": "**", "\\": "/"}

    # Process the file
    markdown_content = process_file(filepath, temp_project_root, MASKER, False, replace)

    # Assert that special characters are handled correctly
    assert "Special chars: USD, **, *, +, ?, ., /" in markdown_content


def test_text_replacement_multiple_occurrences(temp_project_root):
    # Test replacement with multiple occurrences of the same string
    file_content = "test test test"
    filepath = create_dummy_file(temp_project_root, "test_file.txt", file_content)

    # Define replacement
    replace = {"test": "success"}

    # Process the file
    markdown_content = process_file(filepath, temp_project_root, MASKER, False, replace)

    # Assert that all occurrences are replaced
    assert "success success success" in markdown_content
