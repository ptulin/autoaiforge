import pytest
from local_privacy_guard import PrivacyGuard
from unittest.mock import patch

def test_check_no_sensitive_data():
    guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])
    assert guard.check("This is a safe input.") == "This is a safe input."

def test_check_with_sensitive_data():
    guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])
    with pytest.raises(ValueError, match="Sensitive data detected based on privacy rules."):
        guard.check("This contains password.")

def test_wrap_function_no_sensitive_data():
    guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])

    @guard.wrap
    def example_function(input_text):
        return f"Processed: {input_text}"

    assert example_function("Safe input.") == "Processed: Safe input."

def test_wrap_function_with_sensitive_data():
    guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])

    @guard.wrap
    def example_function(input_text):
        return f"Processed: {input_text}"

    with pytest.raises(ValueError, match="Sensitive data detected based on privacy rules."):
        example_function("This contains secret information.")