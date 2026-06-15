import pytest
from unittest.mock import patch, mock_open
from llm_package_optimizer import parse_requirements, optimize_dependencies, check_hardware_compatibility, write_requirements

def test_parse_requirements():
    mock_file_content = "torch\ntensorflow\n# Comment\nscipy\n"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        dependencies = parse_requirements("requirements.txt")
        assert dependencies == ["torch", "tensorflow", "scipy"]

def test_check_hardware_compatibility():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = check_hardware_compatibility()
        assert result == ["torch", "tensorflow-gpu"]

        mock_run.return_value.returncode = 1
        result = check_hardware_compatibility()
        assert result == ["torch-cpu", "tensorflow"]

def test_optimize_dependencies():
    input_deps = ["torch", "tensorflow", "scipy", "numpy"]
    with patch("llm_package_optimizer.check_hardware_compatibility", return_value=["torch", "tensorflow-gpu"]):
        optimized = optimize_dependencies(input_deps)
        assert optimized == ["scipy", "numpy", "torch", "tensorflow-gpu"]

def test_write_requirements():
    dependencies = ["torch", "tensorflow"]
    mock_output = mock_open()
    with patch("builtins.open", mock_output):
        write_requirements(dependencies, "output.txt")
        mock_output().write.assert_any_call("torch\n")
        mock_output().write.assert_any_call("tensorflow\n")