import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from dataset_explorer import analyze_dataset

@patch("dataset_explorer.openai.Completion.create")
def test_analyze_dataset_csv(mock_openai):
    # Mock OpenAI response
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="Mocked analysis result")])

    # Create a mock CSV file
    data = "col1,col2\n1,2\n3,4\n"
    with open("test.csv", "w") as f:
        f.write(data)

    result = analyze_dataset("test.csv", "Summarize the data", "fake_api_key")

    assert result == "Mocked analysis result"

@patch("dataset_explorer.openai.Completion.create")
def test_analyze_dataset_empty(mock_openai):
    # Mock OpenAI response
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="Mocked analysis result")])

    # Create an empty CSV file
    data = "col1,col2\n"
    with open("empty.csv", "w") as f:
        f.write(data)

    result = analyze_dataset("empty.csv", "Summarize the data", "fake_api_key")

    assert result == "The dataset is empty."

@patch("dataset_explorer.openai.Completion.create")
def test_analyze_dataset_invalid_file(mock_openai):
    # Mock OpenAI response
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="Mocked analysis result")])

    with pytest.raises(FileNotFoundError):
        analyze_dataset("nonexistent.csv", "Summarize the data", "fake_api_key")