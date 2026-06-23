import pytest
from unittest.mock import patch, MagicMock
from llm_quant_optimizer import quantize_model, benchmark_model, save_report

def test_quantize_model_invalid_path():
    with pytest.raises(FileNotFoundError):
        quantize_model("invalid/path", "8bit")

def test_quantize_model_invalid_method():
    with pytest.raises(ValueError):
        with patch("os.path.exists", return_value=True):
            quantize_model("valid/path", "16bit")

@patch("llm_quant_optimizer.AutoModelForCausalLM.from_pretrained")
@patch("llm_quant_optimizer.AutoTokenizer.from_pretrained")
@patch("os.path.exists", return_value=True)
def test_quantize_model_valid(mock_exists, mock_tokenizer, mock_model):
    mock_model.return_value = MagicMock()
    mock_tokenizer.return_value = MagicMock()

    model, tokenizer = quantize_model("valid/path", "8bit")
    assert model is not None
    assert tokenizer is not None

@patch("time.time", side_effect=[0, 1])
def test_benchmark_model(mock_time):
    mock_model = MagicMock()
    mock_model.eval = MagicMock()
    mock_model.__call__ = MagicMock()

    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {"input_ids": [1, 2, 3]}

    result = benchmark_model(mock_model, mock_tokenizer)
    assert result == 1

def test_save_report(tmp_path):
    report_data = {"key": "value"}
    output_path = tmp_path / "report.json"

    save_report(report_data, output_path)

    with open(output_path, "r") as f:
        data = f.read()

    assert "key" in data
    assert "value" in data