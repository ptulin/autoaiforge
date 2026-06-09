import pytest
from unittest.mock import patch, MagicMock
from dynamic_llm_router import route_request, get_device_availability

def test_get_device_availability():
    with patch('torch.cuda.is_available', return_value=True), \
         patch('torch.cuda.get_device_properties') as mock_get_device_properties, \
         patch('torch.cuda.memory_allocated', return_value=100):
        mock_get_device_properties.return_value.total_memory = 8000
        with patch('psutil.virtual_memory') as mock_virtual_memory:
            mock_virtual_memory.return_value.available = 16000
            devices = get_device_availability(['cuda', 'cpu'])
            assert 'cuda' in devices
            assert 'cpu' in devices
            assert devices['cuda'] == 7900
            assert devices['cpu'] == 16000

def test_route_request_success():
    input_text = "What is the capital of France?"
    models = ["gpt2"]
    devices = ["cpu"]

    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {"input_ids": [1, 2, 3]}
    mock_model.generate.return_value = [[1, 2, 3]]
    mock_tokenizer.decode.return_value = "Paris"

    with patch('dynamic_llm_router.load_model', return_value=(mock_model, mock_tokenizer)):
        result = route_request(input_text, models, devices)
        assert result['model'] == "gpt2"
        assert result['device'] == "cpu"
        assert result['response'] == "Paris"

def test_route_request_no_devices():
    input_text = "What is the capital of France?"
    models = ["gpt2"]
    devices = []

    with pytest.raises(RuntimeError, match="No available devices."):
        route_request(input_text, models, devices)

def test_route_request_model_failure():
    input_text = "What is the capital of France?"
    models = ["gpt2"]
    devices = ["cpu"]

    with patch('dynamic_llm_router.load_model', side_effect=Exception("Model loading failed")):
        with pytest.raises(RuntimeError, match="Failed to process the request with all available models and devices."):
            route_request(input_text, models, devices)