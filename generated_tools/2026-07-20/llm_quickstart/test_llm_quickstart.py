import pytest
from unittest.mock import patch, MagicMock
from llm_quickstart import detect_hardware, download_model, start_server

def test_detect_hardware():
    with patch("torch.cuda.is_available", return_value=True):
        assert detect_hardware() == "cuda"
    with patch("torch.cuda.is_available", return_value=False):
        assert detect_hardware() == "cpu"

@patch("llm_quickstart.AutoModelForCausalLM.from_pretrained")
@patch("llm_quickstart.AutoTokenizer.from_pretrained")
def test_download_model(mock_tokenizer, mock_model):
    mock_model.return_value = MagicMock()
    mock_tokenizer.return_value = MagicMock()

    model, tokenizer = download_model("EleutherAI/gpt-j-6B", "fp16")
    assert model is not None
    assert tokenizer is not None

@patch("llm_quickstart.Flask.run")
def test_start_server(mock_run):
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    start_server(mock_model, mock_tokenizer, "cpu")
    mock_run.assert_called_once()
