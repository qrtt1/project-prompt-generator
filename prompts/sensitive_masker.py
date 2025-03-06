"""
Module for masking sensitive data in text content.
Identifies and masks patterns containing sensitive information like API keys, passwords, and connection strings.
"""

import re
from typing import List, Optional, Dict
import logging

# Configure logging (optional, can be enabled via CLI or env var)
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Default sensitive data patterns with improved coverage
DEFAULT_SENSITIVE_PATTERNS = [
    # API Keys and Tokens (e.g., api_key="abc123", API_TOKEN=xyz)
    (r'(?i)(api[_-]?key|apikey|api[_-]?token|access[_-]?token|bearer)[\s]*[=:]\s*["\'`]?(?:[^"\'`\s]{6,})["\'`]?',
     "API keys or tokens"),
    # Passwords with quotes (e.g., password="secret123")
    (r'(?i)(password|pwd|pass)[\s]*[=:]\s*["\'`]([^"\'`\s]{6,})["\'`]',
     "Quoted passwords"),
    # Passwords without quotes (e.g., PASSWORD=secret123 in .env)
    (r'(?i)(password|pwd|pass)[\s]*=([^\s"\'`]{6,})',
     "Unquoted passwords"),
    # Connection strings (e.g., mongodb://user:pass@host:port/db)
    (r'(?i)(mongodb|postgresql|mysql|redis|sqlserver):\/\/[^:@\s]+:[^@\s]+@[^\/\s]+(?:\/\S+)?',
     "Database connection strings"),
    # AWS keys (e.g., AKIA1234567890ABCDEF)
    (r'AKIA[0-9A-Z]{16}',
     "AWS access keys"),
    # Generic secrets (e.g., secret_key="xyz", AUTH_TOKEN=abc)
    (r'(?i)(secret|auth)[_-]?(key|token|id|secret)[\s]*[=:]\s*["\'`]?(?:[^"\'`\s]{6,})["\'`]?',
     "Generic secrets"),
    # PowerShell ConvertTo-SecureString (e.g., ConvertTo-SecureString "pass" -AsPlainText)
    (r'(?i)ConvertTo-SecureString\s+(["\'`]).*?\1\s+-AsPlainText',
     "PowerShell secure string with plaintext"),
    (r'(?i)ConvertTo-SecureString\s+-String\s+(["\'`]).*?\1',
     "PowerShell secure string alternative"),
    # SSH private key headers (e.g., -----BEGIN RSA PRIVATE KEY-----)
    (r'-----BEGIN\s+(RSA|OPENSSH|EC)\s+PRIVATE\s+KEY-----[\s\S]+?-----END\s+\1\s+PRIVATE\s+KEY-----',
     "SSH private keys"),
    # Generic long alphanumeric strings (potential tokens or keys)
    (r'(?i)\b[a-z0-9_-]{32,}\b',
     "Long alphanumeric strings (possible tokens)"),
]

# Patterns to exclude (avoid masking documentation or examples)
EXCLUDE_PATTERNS = [
    r'#\s*(example|sample|demo)\s*$',  # Lines marked as examples in comments
    r'//\s*(example|sample|demo)\s*$',  # C-style single-line comments
    r'/\*\s*(example|sample|demo)\s*\*/',  # C-style block comments
]


class SensitiveMasker:
    """Class to handle sensitive data masking operations with improved flexibility."""

    def __init__(self, patterns: Optional[List[tuple]] = None, exclude_patterns: Optional[List[str]] = None):
        """
        Initialize the masker with patterns and optional exclusions.

        Args:
            patterns (List[tuple], optional): List of (pattern, description) tuples. Defaults to DEFAULT_SENSITIVE_PATTERNS.
            exclude_patterns (List[str], optional): Patterns to exclude from masking (e.g., examples).
        """
        self.patterns = patterns if patterns is not None else DEFAULT_SENSITIVE_PATTERNS
        self.exclude_patterns = exclude_patterns if exclude_patterns is not None else EXCLUDE_PATTERNS
        self.compiled_patterns = [(re.compile(p, re.MULTILINE), desc) for p, desc in self.patterns]
        self.compiled_exclusions = [re.compile(p, re.MULTILINE) for p in self.exclude_patterns]

    def add_pattern(self, pattern: str, description: str = "Custom pattern"):
        """Add a new pattern to the masker."""
        self.patterns.append((pattern, description))
        self.compiled_patterns.append((re.compile(pattern, re.MULTILINE), description))

    def mask_content(self, content: str, context_window: int = 100) -> str:
        """
        Mask sensitive data in the content with context-aware exclusion.

        Args:
            content (str): Text content to mask.
            context_window (int): Number of characters to check around a match for exclusions.

        Returns:
            str: Content with sensitive data masked.
        """
        masked_content = content
        masked_count = 0

        for pattern, desc in self.compiled_patterns:
            def mask_match(match):
                nonlocal masked_count
                start, end = match.start(), match.end()
                # Check context for exclusions
                context_start = max(0, start - context_window)
                context_end = min(len(content), end + context_window)
                context = content[context_start:context_end]

                if any(exclude.search(context) for exclude in self.compiled_exclusions):
                    return match.group(0)  # Skip masking if in an excluded context

                # Special handling for specific cases
                full_match = match.group(0)
                if 'ConvertTo-SecureString' in full_match:
                    pwd_match = re.search(r'(["\'`])(.*?)\1', full_match)
                    if pwd_match:
                        quoted_pwd = pwd_match.group(0)
                        pwd_content = pwd_match.group(2)
                        masked_pwd = pwd_match.group(1) + '*' * len(pwd_content) + pwd_match.group(1)
                        return full_match.replace(quoted_pwd, masked_pwd)

                # Handle key-value pairs (both quoted and unquoted)
                if '=' in full_match:
                    # Use regex to split while preserving spacing and quotes
                    key_value_match = re.match(r'^(.*?)(\s*=)(\s*["\'`]?)(.*?)(["\'`]?\s*)$', full_match)
                    if key_value_match:
                        key_part = key_value_match.group(1)  # e.g., "password"
                        equals_part = key_value_match.group(2)  # e.g., " ="
                        quote_prefix = key_value_match.group(3)  # e.g., " "
                        value_part = key_value_match.group(4)  # e.g., "supersecret"
                        quote_suffix = key_value_match.group(5)  # e.g., ""
                        if quote_prefix.strip() and quote_prefix.strip() in '"\'`':
                            quote = quote_prefix.strip()
                            return f"{key_part}{equals_part}{quote}{'*' * len(value_part)}{quote}"
                        else:
                            return f"{key_part}{equals_part}{'*' * len(value_part)}"

                # Default: mask the entire match
                masked_count += 1
                logger.debug(f"Masked {desc}: {full_match}")
                return '*' * len(full_match)

            masked_content = pattern.sub(mask_match, masked_content)

        if masked_count > 0:
            logger.info(f"Masked {masked_count} sensitive items in content")
        return masked_content

    @classmethod
    def from_config(cls, config_file: str) -> 'SensitiveMasker':
        """Load patterns from a config file (e.g., JSON or YAML)."""
        # Placeholder for future extension (e.g., read from a file)
        return cls()


def mask_sensitive_data(content: str, patterns: Optional[List[tuple]] = None) -> str:
    """
    Utility function to mask sensitive data in content.

    Args:
        content (str): The content to mask.
        patterns (List[tuple], optional): Custom (pattern, description) tuples.

    Returns:
        str: Content with sensitive data masked.
    """
    masker = SensitiveMasker(patterns)
    return masker.mask_content(content)


# Example usage
if __name__ == "__main__":
    test_content = """
    api_key="sk-abc1234567890"
    PASSWORD=secret123
    mongodb://admin:pass123@host:27017/db
    AKIA1234567890ABCDEF
    # Example: api_key="fakekey" (should not mask)
    ConvertTo-SecureString "myp@ssw0rd" -AsPlainText
    random_string="not-a-secret"
    """
    masked = mask_sensitive_data(test_content)
    print(masked)