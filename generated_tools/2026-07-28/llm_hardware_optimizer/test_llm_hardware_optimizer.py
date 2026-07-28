import pytest
from unittest.mock import patch, MagicMock
from llm_hardware_optimizer import profile_hardware, generate_configuration, save_configuration
import os
import yaml

def test_profile_hardware():
    with patch("torch.cuda.is_available", return_value=True), \
         patch("torch.cuda.device_count", return_value=2), \
         patch("torch.cuda.get_device_properties") as mock_props:
        mock_props.return_value = MagicMock(name="MockGPU", total_memory=16 * 1024 ** 3, major=7, minor=5)

        hardware_info = profile_hardware()
        assert hardware_info["gpu_available"] is True
        assert hardware_info["gpu_count"] == 2
        assert len(hardware_info["gpu_details"]) == 2

def test_generate_configuration():
    hardware_info = {
        "gpu_available": True,
        "gpu_count": 1,
        "gpu_details": [{"memory_gb": 8, "name": "MockGPU", "compute_capability": "7.5"}],
        "total_memory_gb": 16
    }
    config = generate_configuration(hardware_info)
    assert config["precision"] == "FP16"
    assert config["batch_size"] == 32
    assert config["parallelism"] == "none"

def test_save_configuration(tmp_path):
    config = {"batch_size": 32, "precision": "FP16", "parallelism": "none"}
    output_path = tmp_path / "config.yaml"

    save_configuration(config, str(output_path))

    with open(output_path, "r") as file:
        loaded_config = yaml.safe_load(file)

    assert loaded_config == config
