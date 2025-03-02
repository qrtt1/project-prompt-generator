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

def test_mask_convertto_securestring():
    # Test PowerShell ConvertTo-SecureString with plaintext
    text = 'ConvertTo-SecureString "P@$$wOrd" -AsPlainText'
    masked = mask_sensitive_data(text)
    assert 'ConvertTo-SecureString "********" -AsPlainText' in masked
    assert 'P@$$wOrd' not in masked

def test_mask_convertto_securestring_alternative():
    # Test PowerShell ConvertTo-SecureString with alternative syntax
    text = 'ConvertTo-SecureString -String "anotherSecret"'
    masked = mask_sensitive_data(text)
    assert 'ConvertTo-SecureString -String "*************"' in masked
    assert 'anotherSecret' not in masked

def test_mask_convertto_securestring_complex():
    # Test PowerShell ConvertTo-SecureString with more complex password
    text = 'ConvertTo-SecureString "Complex-P@$$wOrd123!" -AsPlainText'
    masked = mask_sensitive_data(text)
    assert 'ConvertTo-SecureString "********************" -AsPlainText' in masked
    assert 'Complex-P@$$wOrd123!' not in masked
