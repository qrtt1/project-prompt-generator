"""
Module for masking sensitive data in text content.
This provides functionality to identify and mask patterns that might contain
sensitive information like API keys, passwords, and connection strings.
"""

import re

# Default sensitive data patterns to mask
DEFAULT_SENSITIVE_PATTERNS = [
    # API Keys and Tokens
    r'(api[_-]?key|apikey|api[_-]?token|access[_-]?token)[\s]*[=:]\s*["\'`]([^"\'`\s]+)["\'`]',
    # Passwords
    r'(password|passwd|pwd)[\s]*[=:]\s*["\'`]([^"\'`\s]+)["\'`]',
    # Connection strings
    r'(mongodb|postgresql|mysql|redis):\/\/[^\s\"\'`]+',
    # AWS keys
    r'(AKIA[0-9A-Z]{16})',
    # Generic secrets
    r'(secret|auth)[_-]?(key|token)[\s]*[=:]\s*["\'`]([^"\'`\s]+)["\'`]',
]


class SensitiveMasker:
    """Class to handle sensitive data masking operations."""

    def __init__(self, patterns=None):
        """
        Initialize the masker with given patterns.

        Args:
            patterns (list, optional): List of regex patterns to use for masking.
                                       Defaults to DEFAULT_SENSITIVE_PATTERNS.
        """
        self.patterns = patterns if patterns is not None else DEFAULT_SENSITIVE_PATTERNS.copy()

    def add_pattern(self, pattern):
        """
        Add a new pattern to the masker.

        Args:
            pattern (str): Regex pattern to add
        """
        self.patterns.append(pattern)

    def mask_content(self, content):
        """
        Mask sensitive data in the content.

        Args:
            content (str): Text content to mask

        Returns:
            str: Content with sensitive data masked
        """
        masked_content = content

        for pattern in self.patterns:
            # Apply the masking for this pattern
            masked_content = self._apply_mask_for_pattern(masked_content, pattern)

        return masked_content

    def _apply_mask_for_pattern(self, content, pattern):
        """
        Apply masking for a specific pattern.

        Args:
            content (str): Text content to mask
            pattern (str): Regex pattern to match

        Returns:
            str: Content with this pattern masked
        """

        # Function to replace matches with asterisks
        def mask_match(match):
            # Get the full match
            full_match = match.group(0)

            # If there are capture groups, we want to keep the variable names but mask the values
            if len(match.groups()) > 0:
                if '=' in full_match or ':' in full_match:
                    # Split by the assignment operator
                    parts = re.split(r'([=:]\s*["\'`])', full_match, 1)
                    if len(parts) >= 3:
                        # Keep the variable name and assignment operator, mask just the value
                        masked_value = '*' * len(parts[2].rstrip('"\'\`'))
                        return parts[0] + parts[1] + masked_value + parts[2][-1] if parts[2] else parts[0] + parts[
                            1] + masked_value

            # For simple matches like AWS keys, just mask the entire match
            return '*' * len(full_match)

        # Apply the masking
        return re.sub(pattern, mask_match, content)


def mask_sensitive_data(content, patterns=None):
    """
    Utility function to mask sensitive data in content.

    Args:
        content (str): The content to search for sensitive data
        patterns (list, optional): List of regex patterns to match.
                                  Defaults to DEFAULT_SENSITIVE_PATTERNS.

    Returns:
        str: Content with sensitive data masked
    """
    masker = SensitiveMasker(patterns)
    return masker.mask_content(content)
