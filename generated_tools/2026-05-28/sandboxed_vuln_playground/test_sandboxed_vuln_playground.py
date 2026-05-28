import pytest
from unittest.mock import patch, mock_open, Mock
import os
from sandboxed_vuln_playground import run_script_in_sandbox

def test_run_script_in_sandbox_no_llm():
    script_content = "print('Hello, World!')"
    with patch("builtins.open", mock_open(read_data=script_content)):
        with patch("os.path.exists", return_value=True):
            with patch("sandboxed_vuln_playground.Sandbox.run") as mock_run:
                mock_run.return_value = Mock(stdout="Hello, World!\n", stderr="")
                result = run_script_in_sandbox("dummy_script.py")
                assert "Hello, World!" in result["output"]
                assert result["error"] == ""

def test_run_script_in_sandbox_with_llm():
    script_content = "print('Hello, World!')"
    with patch("builtins.open", mock_open(read_data=script_content)):
        with patch("os.path.exists", return_value=True):
            with patch("sandboxed_vuln_playground.Sandbox.run") as mock_run:
                mock_run.return_value = Mock(stdout="Hello, World!\nInjected vulnerability\n", stderr="")
                result = run_script_in_sandbox("dummy_script.py", "Inject vulnerability")
                assert "Hello, World!" in result["output"]
                assert "Injected vulnerability" in result["output"]
                assert result["error"] == ""

def test_run_script_in_sandbox_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            run_script_in_sandbox("non_existent_script.py")