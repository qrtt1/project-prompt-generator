"""
Tests for the sensitive_masker module.
"""

import pytest
from prompts.sensitive_masker import SensitiveMasker, mask_sensitive_data

def test_mask_api_key():
    # Test basic API key masking
    text = 'api_key="abcdefg123456"'
    masked = mask_sensitive_data(text)
    assert 'api_key="*************"' in masked
    assert 'abcdefg123456' not in masked

def test_mask_password():
    # Test password masking
    text = 'password = "supersecret"'
    masked = mask_sensitive_data(text)
    assert 'password = "***********"' in masked
    assert 'supersecret' not in masked

def test_no_sensitive_data():
    # Test text without sensitive data
    text = 'This is just normal text with no secrets'
    masked = mask_sensitive_data(text)
    assert masked == text  # Should be unchanged
