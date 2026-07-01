import pytest
from unittest.mock import patch, MagicMock
from gpu_gemm_optimizer import analyze_and_optimize_gemm

def test_analyze_and_optimize_gemm_cuda():
    with patch('importlib.import_module') as mock_import:
        mock_cupy = MagicMock()
        mock_import.return_value = mock_cupy

        mock_cupy.array.return_value = MagicMock()
        mock_cupy.dot.return_value = MagicMock(shape=(512, 256))
        mock_cupy.cuda.Device.return_value = MagicMock()
        mock_event_instance = MagicMock()
        mock_event_instance.record = MagicMock()
        mock_event_instance.synchronize = MagicMock()
        mock_event_instance.elapsed_time = MagicMock(return_value=1000)
        mock_cupy.cuda.Event.side_effect = lambda: mock_event_instance

        result = analyze_and_optimize_gemm(512, 256, 128, 'cuda')
        assert 'optimized_block_size' in result
        assert 'performance_seconds' in result
        assert 'result_shape' in result
        assert result['result_shape'] == (512, 256)

def test_analyze_and_optimize_gemm_rocm():
    with patch('importlib.import_module') as mock_import:
        mock_torch = MagicMock()
        mock_import.return_value = mock_torch

        mock_torch.tensor.return_value = MagicMock()
        mock_torch.mm.return_value = MagicMock(shape=(512, 256))
        mock_torch.cuda.synchronize = MagicMock()
        mock_event_instance = MagicMock()
        mock_event_instance.record = MagicMock()
        mock_event_instance.synchronize = MagicMock()
        mock_event_instance.elapsed_time = MagicMock(return_value=1000)
        mock_torch.cuda.Event.side_effect = lambda enable_timing: mock_event_instance

        result = analyze_and_optimize_gemm(512, 256, 128, 'rocm')
        assert 'optimized_block_size' in result
        assert 'performance_seconds' in result
        assert 'result_shape' in result
        assert result['result_shape'] == (512, 256)

def test_invalid_device():
    with pytest.raises(ValueError):
        analyze_and_optimize_gemm(512, 256, 128, 'invalid_device')
