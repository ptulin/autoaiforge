import pytest
import json
from unittest.mock import patch, MagicMock
from llm_batch_infer_tool import load_input, save_output, chunk_input, batch_inference

def test_load_input_text_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("line1\nline2\nline3\n")
    result = load_input(str(test_file))
    assert result == ["line1", "line2", "line3"]

def test_load_input_json_file(tmp_path):
    test_file = tmp_path / "test.json"
    test_file.write_text(json.dumps(["input1", "input2", "input3"]))
    result = load_input(str(test_file))
    assert result == ["input1", "input2", "input3"]

def test_chunk_input():
    data = ["input1", "input2", "input3", "input4"]
    result = chunk_input(data, 2)
    assert result == [["input1", "input2"], ["input3", "input4"]]

def test_batch_inference():
    input_data = ["input1", "input2", "input3"]
    mock_pipeline = MagicMock()
    mock_pipeline.side_effect = lambda batch, max_length: [
        {"generated_text": f"output_{text}"} for text in batch
    ]

    with patch("llm_batch_infer_tool.pipeline", return_value=mock_pipeline):
        result = batch_inference(input_data, batch_size=2, parallel=1)
        assert result == ["output_input1", "output_input2", "output_input3"]
