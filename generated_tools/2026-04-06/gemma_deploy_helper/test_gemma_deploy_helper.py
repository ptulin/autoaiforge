import pytest
from unittest.mock import patch, MagicMock
from gemma_deploy_helper import detect_hardware, download_model, launch_server

def test_detect_hardware_cpu():
    assert detect_hardware('cpu') == 'cpu'

def test_detect_hardware_gpu_available():
    with patch('torch.cuda.is_available', return_value=True):
        assert detect_hardware('gpu') == 'cuda'

def test_detect_hardware_gpu_unavailable():
    with patch('torch.cuda.is_available', return_value=False):
        assert detect_hardware('gpu') == 'cpu'

def test_download_model_success():
    with patch('transformers.AutoModelForCausalLM.from_pretrained') as mock_model, \
         patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer:
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()
        model, tokenizer = download_model('gemma-4')
        assert model is not None
        assert tokenizer is not None

def test_download_model_failure():
    with patch('transformers.AutoModelForCausalLM.from_pretrained', side_effect=Exception("Download error")):
        with pytest.raises(SystemExit):
            download_model('invalid-model')

def test_launch_server():
    with patch('logging.info') as mock_logging:
        model = MagicMock()
        tokenizer = MagicMock()
        launch_server(model, tokenizer, 'cpu', 1, 8080)
        mock_logging.assert_called_with("Server is running. Press Ctrl+C to stop.")