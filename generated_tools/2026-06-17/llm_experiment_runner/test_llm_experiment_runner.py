import pytest
from unittest.mock import patch, MagicMock
from llm_experiment_runner import load_model, run_inference, compute_metrics, load_dataset

def test_load_model():
    with patch('llm_experiment_runner.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('llm_experiment_runner.AutoModelForCausalLM.from_pretrained') as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        model, tokenizer = load_model("test-model")

        assert model is not None
        assert tokenizer is not None
        mock_tokenizer.assert_called_once_with("test-model")
        mock_model.assert_called_once_with("test-model")

def test_run_inference():
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {"input_ids": [1, 2, 3]}
    mock_model.generate.return_value = [[4, 5, 6]]
    mock_tokenizer.decode.return_value = "Generated text"

    dataset = ["Test input"]
    results, latencies = run_inference(mock_model, mock_tokenizer, dataset)

    assert len(results) == 1
    assert results[0]["input"] == "Test input"
    assert results[0]["output"] == "Generated text"
    assert "latency" in results[0]
    assert len(latencies) == 1

def test_compute_metrics():
    latencies = [0.1, 0.2, 0.3]
    metrics = compute_metrics(latencies)

    assert metrics["mean_latency"] == pytest.approx(0.2)
    assert metrics["max_latency"] == pytest.approx(0.3)
    assert metrics["min_latency"] == pytest.approx(0.1)

def test_load_dataset(tmp_path):
    dataset_path = tmp_path / "test_dataset.txt"
    dataset_path.write_text("line1\nline2\n\nline3\n")

    dataset = load_dataset(str(dataset_path))

    assert dataset == ["line1", "line2", "line3"]

def test_load_dataset_file_not_found():
    with pytest.raises(RuntimeError, match="Dataset file 'nonexistent.txt' not found."):
        load_dataset("nonexistent.txt")
