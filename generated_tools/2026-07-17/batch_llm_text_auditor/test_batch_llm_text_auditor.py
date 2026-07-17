import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from batch_llm_text_auditor import BatchLLMTextAuditor

@pytest.fixture
def mock_auditor(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_file = tmp_path / "output.csv"
    return BatchLLMTextAuditor(input_dir=str(input_dir), output_file=str(output_file))

def test_preprocess_text(mock_auditor):
    text = "Hello, World! This is a test."
    expected = "hello world test"
    assert mock_auditor.preprocess_text(text) == expected

def test_load_data(mock_auditor):
    # Create mock text files
    file1 = os.path.join(mock_auditor.input_dir, "file1.txt")
    with open(file1, "w") as f:
        f.write("This is a test file.")
    file2 = os.path.join(mock_auditor.input_dir, "file2.txt")
    with open(file2, "w") as f:
        f.write("Another test file.")

    filenames, texts = mock_auditor.load_data()
    assert sorted(filenames) == ["file1.txt", "file2.txt"]
    assert sorted(texts) == ["Another test file.", "This is a test file."]

@patch("batch_llm_text_auditor.BatchLLMTextAuditor.train_model")
@patch("batch_llm_text_auditor.BatchLLMTextAuditor.classify_texts")
def test_run(mock_classify_texts, mock_train_model, mock_auditor):
    # Mock methods
    mock_classify_texts.return_value = [0.1, 0.9]
    mock_train_model.return_value = None

    # Create mock text files
    file1 = os.path.join(mock_auditor.input_dir, "file1.txt")
    with open(file1, "w") as f:
        f.write("This is a test file.")
    file2 = os.path.join(mock_auditor.input_dir, "file2.txt")
    with open(file2, "w") as f:
        f.write("Another test file.")

    mock_auditor.run()

    # Check output CSV
    output_df = pd.read_csv(mock_auditor.output_file)
    assert len(output_df) == 2
    assert "Filename" in output_df.columns
    assert "LLM_Probability" in output_df.columns
    assert "LLM_Prediction" in output_df.columns
