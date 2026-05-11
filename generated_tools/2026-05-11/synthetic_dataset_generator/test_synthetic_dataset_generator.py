import pytest
from unittest.mock import patch, MagicMock
from synthetic_dataset_generator import generate_synthetic_data
import json
import os

def mock_openai_completion_create(*args, **kwargs):
    class MockChoice:
        def __init__(self, text):
            self.text = text

    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice("Generated sample data")]

    return MockResponse()

@patch('synthetic_dataset_generator.openai.Completion.create', side_effect=mock_openai_completion_create)
def test_generate_synthetic_data_json(mock_openai):
    api_key = "test_api_key"
    prompt = "Generate a list of product descriptions"
    count = 5
    output_format = "json"

    output_file = generate_synthetic_data(api_key, prompt, count, output_format)

    with open(output_file, 'r') as f:
        data = json.load(f)

    assert len(data) == count
    assert data[0] == "Generated sample data"

    os.remove(output_file)  # Clean up the generated file

@patch('synthetic_dataset_generator.openai.Completion.create', side_effect=mock_openai_completion_create)
def test_generate_synthetic_data_csv(mock_openai):
    api_key = "test_api_key"
    prompt = "Generate a list of product descriptions"
    count = 5
    output_format = "csv"

    output_file = generate_synthetic_data(api_key, prompt, count, output_format)

    import pandas as pd
    df = pd.read_csv(output_file)

    assert len(df) == count
    assert df.iloc[0, 0] == "Generated sample data"

    os.remove(output_file)  # Clean up the generated file

@patch('synthetic_dataset_generator.openai.Completion.create', side_effect=mock_openai_completion_create)
def test_generate_synthetic_data_invalid_count(mock_openai):
    api_key = "test_api_key"
    prompt = "Generate a list of product descriptions"
    count = -1
    output_format = "json"

    with pytest.raises(ValueError, match="Count must be a positive integer."):
        generate_synthetic_data(api_key, prompt, count, output_format)

@patch('synthetic_dataset_generator.openai.Completion.create', side_effect=mock_openai_completion_create)
def test_generate_synthetic_data_invalid_format(mock_openai):
    api_key = "test_api_key"
    prompt = "Generate a list of product descriptions"
    count = 5
    output_format = "xml"

    with pytest.raises(ValueError, match="Output format must be either 'csv' or 'json'."):
        generate_synthetic_data(api_key, prompt, count, output_format)
