import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from claude_memory_importer import upload_memory_snippets, validate_and_sanitize_data

def test_validate_and_sanitize_data():
    # Test valid data
    valid_data = pd.DataFrame({
        'id': [1, 2, 3],
        'content': ['Memory 1', 'Memory 2', 'Memory 3']
    })
    sanitized_data = validate_and_sanitize_data(valid_data)
    assert len(sanitized_data) == 3

    # Test missing required column
    invalid_data = pd.DataFrame({
        'content': ['Memory 1', 'Memory 2', 'Memory 3']
    })
    with pytest.raises(ValueError, match="Missing required column: id"):
        validate_and_sanitize_data(invalid_data)

    # Test duplicate IDs
    duplicate_data = pd.DataFrame({
        'id': [1, 1, 2],
        'content': ['Memory 1', 'Memory 2', 'Memory 3']
    })
    with pytest.raises(ValueError, match="Duplicate IDs found in the input data."):
        validate_and_sanitize_data(duplicate_data)

@patch('claude_memory_importer.MockAnthropic')
def test_upload_memory_snippets(mock_anthropic):
    # Mock the API client
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client

    # Mock API responses
    mock_client.create_memory.side_effect = [
        {"status": "success"},
        Exception("API error"),
        {"status": "success"}
    ]

    # Test data
    test_data = pd.DataFrame({
        'id': [1, 2, 3],
        'content': ['Memory 1', 'Memory 2', 'Memory 3']
    })
    test_file_path = 'test.json'
    test_data.to_json(test_file_path, orient='records', lines=True)

    try:
        # Run the function
        results = upload_memory_snippets(test_file_path, 'test_api_key')

        # Validate results
        assert len(results) == 3
        assert results[0]['status'] == 'success'
        assert results[1]['status'] == 'error'
        assert 'API error' in results[1]['error']
        assert results[2]['status'] == 'success'
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.remove(test_file_path)