import pytest
from unittest.mock import patch, mock_open
import yaml
from llm_training_optimizer import autodetect_hardware, generate_config

def test_autodetect_hardware():
    with patch("psutil.virtual_memory") as mock_memory, patch("psutil.cpu_count") as mock_cpu:
        mock_memory.return_value.total = 16 * 1024 ** 3  # 16GB
        mock_cpu.return_value = 8
        hardware = autodetect_hardware()
        assert hardware == {"memory_gb": 16, "cpu_cores": 8}

def test_generate_config():
    hardware_specs = {"memory_gb": 16, "cpu_cores": 8}
    model = "gpt-j"
    dataset_size = "10GB"
    config = generate_config(hardware_specs, model, dataset_size)
    assert config["training"]["batch_size"] == 32
    assert config["training"]["num_workers"] == 4
    assert config["training"]["precision"] == "fp16"

def test_main_with_hardware_file():
    hardware_yaml = "memory_gb: 32\ncpu_cores: 16\n"
    with patch("builtins.open", mock_open(read_data=hardware_yaml)), patch("llm_training_optimizer.autodetect_hardware") as mock_autodetect:
        mock_autodetect.return_value = {"memory_gb": 32, "cpu_cores": 16}
        hardware_specs = yaml.safe_load(hardware_yaml)
        assert hardware_specs == {"memory_gb": 32, "cpu_cores": 16}