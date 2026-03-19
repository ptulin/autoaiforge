import pytest
import json
import yaml
from unittest.mock import mock_open, patch
from dlss_integration_checker import check_dlss_compatibility

def test_valid_yaml_config():
    mock_yaml = """
    rendering_api: directx12
    gpu: nvidia rtx 3080
    rendering_pipeline:
      type: deferred
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        result = check_dlss_compatibility("config.yaml")
        assert result["rendering_api"] == "Supported API: directx12."
        assert result["gpu"] == "Supported GPU: nvidia rtx 3080."
        assert result["rendering_pipeline"] == "Supported rendering pipeline: deferred."
        assert "debugging_tips" not in result

def test_invalid_api():
    mock_yaml = """
    rendering_api: opengl
    gpu: nvidia rtx 3080
    rendering_pipeline:
      type: deferred
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        result = check_dlss_compatibility("config.yaml")
        assert result["rendering_api"] == "Unsupported API: opengl. Use DirectX 12 or Vulkan."
        assert "debugging_tips" in result

def test_missing_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = check_dlss_compatibility("nonexistent.yaml")
        assert result == {"error": "Configuration file not found."}

def test_invalid_file_format():
    mock_invalid_yaml = "invalid_yaml: [unclosed_bracket"
    with patch("builtins.open", mock_open(read_data=mock_invalid_yaml)):
        result = check_dlss_compatibility("config.yaml")
        assert result == {"error": "Invalid configuration file format."}

def test_unsupported_gpu():
    mock_yaml = """
    rendering_api: vulkan
    gpu: amd radeon
    rendering_pipeline:
      type: forward
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        result = check_dlss_compatibility("config.yaml")
        assert result["gpu"] == "Unsupported GPU: amd radeon. NVIDIA GPUs are required for DLSS."
        assert "debugging_tips" in result