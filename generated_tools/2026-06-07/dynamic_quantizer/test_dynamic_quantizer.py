import pytest
from unittest.mock import patch, MagicMock
from dynamic_quantizer import quantify_model
import torch

def test_quantify_model_with_valid_method():
    model = MagicMock(spec=torch.nn.Module)
    result = quantify_model(model, method='GPTQ', monitor_resources=False)
    assert 'quantized_model' in result
    assert 'time_taken' in result

def test_quantify_model_with_invalid_method():
    model = MagicMock(spec=torch.nn.Module)
    with pytest.raises(ValueError, match="Unsupported quantization method"):
        quantify_model(model, method='INVALID', monitor_resources=False)

@patch('psutil.cpu_percent', return_value=10.0)
@patch('psutil.virtual_memory')
def test_quantify_model_with_resource_monitoring(mock_virtual_memory, mock_cpu_percent):
    mock_virtual_memory.return_value = MagicMock(_asdict=lambda: {'total': 8000, 'available': 4000})
    model = MagicMock(spec=torch.nn.Module)
    result = quantify_model(model, method='GPTQ', monitor_resources=True)
    assert 'resource_stats' in result
    assert 'before' in result['resource_stats']
    assert 'after' in result['resource_stats']
    assert result['resource_stats']['before']['cpu_percent'] == 10.0
    assert result['resource_stats']['after']['cpu_percent'] == 10.0