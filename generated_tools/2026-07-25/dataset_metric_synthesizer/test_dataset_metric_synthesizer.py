import pytest
import pandas as pd
from dataset_metric_synthesizer import generate_dataset, custom_metric, save_dataset
from unittest.mock import patch, mock_open, MagicMock
import os

def test_generate_dataset():
    dataset = generate_dataset(vocab_size=50, num_samples=10, sentence_length=5)
    assert len(dataset) == 10
    assert "text" in dataset.columns

def test_custom_metric():
    dataset = generate_dataset(vocab_size=50, num_samples=10, sentence_length=5)

    def mock_metric(text):
        return len(text.split())

    scored_dataset = custom_metric(dataset, mock_metric)
    assert "score" in scored_dataset.columns
    assert all(scored_dataset["score"] == 5)

def test_save_dataset():
    dataset = generate_dataset(vocab_size=50, num_samples=10, sentence_length=5)
    file_path = "test_output.csv"

    try:
        save_dataset(dataset, file_path, format="csv")
        assert os.path.exists(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@pytest.mark.parametrize("invalid_params", [
    (0, 10, 5),
    (50, -10, 5),
    (50, 10, -5)
])
def test_generate_dataset_invalid_params(invalid_params):
    vocab_size, num_samples, sentence_length = invalid_params
    with pytest.raises(ValueError):
        generate_dataset(vocab_size, num_samples, sentence_length)

@patch("pandas.DataFrame.to_json")
def test_save_dataset_json(mock_to_json):
    dataset = generate_dataset(vocab_size=50, num_samples=10, sentence_length=5)
    file_path = "test_output.json"

    save_dataset(dataset, file_path, format="json")
    mock_to_json.assert_called_once_with(file_path, orient="records", lines=True)
