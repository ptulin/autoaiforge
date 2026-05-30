import pytest
from unittest.mock import patch, MagicMock
from gpu_utilization_calculator import monitor_gpu_utilization, run_inference

def test_monitor_gpu_utilization():
    with patch('GPUtil.getGPUs') as mock_get_gpus:
        mock_gpu = MagicMock()
        mock_gpu.load = 0.5
        mock_get_gpus.return_value = [mock_gpu]

        utilization = monitor_gpu_utilization(duration=2, interval=0.5, output_file='test_output.png')

        assert len(utilization) == 4  # 2 seconds / 0.5 interval = 4 samples
        assert all(u == 50.0 for u in utilization)  # Mocked GPU load is 50%

def test_run_inference_success():
    with patch('torch.hub.load') as mock_torch_hub:
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = 'encoded_input'
        mock_model.generate.return_value = ['generated_output']
        mock_tokenizer.decode.return_value = 'decoded_output'

        mock_torch_hub.side_effect = [mock_model, mock_tokenizer]

        output = run_inference('gpt-2', 'Hello, world!')

        assert output == 'decoded_output'
        mock_tokenizer.encode.assert_called_once_with('Hello, world!', return_tensors='pt')
        mock_model.generate.assert_called_once_with('encoded_input', max_length=50)

def test_run_inference_failure():
    with patch('torch.hub.load', side_effect=RuntimeError('Model not found')):
        with pytest.raises(RuntimeError, match="Error during inference: Model not found"):
            run_inference('nonexistent-model', 'Hello, world!')