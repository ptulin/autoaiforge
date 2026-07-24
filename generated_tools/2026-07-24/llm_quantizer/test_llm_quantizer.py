import pytest
import torch
from unittest.mock import patch, MagicMock
from llm_quantizer import quantize_model

@pytest.fixture
def mock_model():
    # Create a simple mock model
    return torch.nn.Sequential(torch.nn.Linear(10, 5))

@patch('torch.load')
@patch('torch.save')
def test_dynamic_quantization(mock_save, mock_load, mock_model):
    mock_load.return_value = mock_model

    # Call the function
    quantize_model('mock_model.pth', 'dynamic', 'quantized_model.pth')

    # Assertions
    mock_load.assert_called_once_with('mock_model.pth')
    mock_save.assert_called_once()

@patch('torch.load')
@patch('torch.save')
def test_static_quantization(mock_save, mock_load, mock_model):
    mock_load.return_value = mock_model

    # Call the function
    quantize_model('mock_model.pth', 'static', 'quantized_model.pth')

    # Assertions
    mock_load.assert_called_once_with('mock_model.pth')
    mock_save.assert_called_once()

@patch('torch.load')
@patch('torch.save')
def test_invalid_quantization_type(mock_save, mock_load, mock_model):
    mock_load.return_value = mock_model

    # Call the function with invalid quantization type
    with pytest.raises(ValueError, match="Unsupported quantization type."):
        quantize_model('mock_model.pth', 'invalid', 'quantized_model.pth')

    # Assertions
    mock_load.assert_called_once_with('mock_model.pth')
    mock_save.assert_not_called()