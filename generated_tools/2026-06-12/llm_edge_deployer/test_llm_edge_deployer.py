import pytest
from unittest.mock import patch, MagicMock, mock_open
import numpy as np
import json
from llm_edge_deployer import convert_to_onnx, check_device_compatibility, run_test_inference

def test_convert_to_onnx():
    with patch("optimum.onnxruntime.ORTModel.from_pretrained") as mock_from_pretrained:
        mock_model = MagicMock()
        mock_from_pretrained.return_value = mock_model
        mock_model.save_pretrained.return_value = None

        result = convert_to_onnx("mock_input_model.bin", "mock_output_model.onnx")
        assert result == "mock_output_model.onnx"
        mock_model.save_pretrained.assert_called_once_with("mock_output_model.onnx")

def test_check_device_compatibility():
    assert check_device_compatibility("tensorrt") is True
    assert check_device_compatibility("openvino") is True
    with pytest.raises(ValueError):
        check_device_compatibility("unsupported_device")

def test_run_test_inference():
    with patch("onnxruntime.InferenceSession") as mock_inference_session:
        mock_session = MagicMock()
        mock_inference_session.return_value = mock_session
        mock_input = MagicMock()
        mock_input.name = "input_name"
        mock_session.get_inputs.return_value = [mock_input]
        mock_session.run.return_value = [np.array([1, 2, 3])]

        test_sample = [0.5, 0.6, 0.7]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_sample))):
            result = run_test_inference("mock_model.onnx", "mock_sample.json")
            assert len(result) == 1
            assert np.array_equal(result[0], np.array([1, 2, 3]))
            mock_session.run.assert_called_once()
            np.testing.assert_array_equal(
                mock_session.run.call_args[0][1]["input_name"], np.array(test_sample, dtype=np.float32)
            )
