import pytest
from unittest.mock import patch, mock_open
import subprocess
from llm_code_eval import run_code_with_interpreter

def test_run_code_with_interpreter_success():
    with patch("builtins.open", mock_open(read_data="expected output")):
        with patch("os.path.exists", side_effect=lambda path: True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = subprocess.CompletedProcess(
                    args=["interpreter", "code"],
                    returncode=0,
                    stdout="expected output",
                    stderr=""
                )

                result = run_code_with_interpreter("code.bf", "interpreter", "expected.txt")

                assert result["success"] is True
                assert result["output"] == "expected output"
                assert result["error"] == ""
                assert result["expected_output"] == "expected output"

def test_run_code_with_interpreter_file_not_found():
    with patch("os.path.exists", side_effect=lambda path: path != "missing_code.bf"):
        result = run_code_with_interpreter("missing_code.bf", "interpreter", "expected.txt")
        assert result["success"] is False
        assert result["error"] == "Code file not found."

def test_run_code_with_interpreter_execution_error():
    with patch("builtins.open", mock_open(read_data="expected output")):
        with patch("os.path.exists", side_effect=lambda path: True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = subprocess.CompletedProcess(
                    args=["interpreter", "code"],
                    returncode=1,
                    stdout="",
                    stderr="Runtime error"
                )

                result = run_code_with_interpreter("code.bf", "interpreter", "expected.txt")

                assert result["success"] is False
                assert result["output"] == ""
                assert result["error"] == "Runtime error"
                assert result["expected_output"] == "expected output"

def test_run_code_with_interpreter_timeout():
    with patch("builtins.open", mock_open(read_data="expected output")):
        with patch("os.path.exists", side_effect=lambda path: True):
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="interpreter", timeout=10)):
                result = run_code_with_interpreter("code.bf", "interpreter", "expected.txt")

                assert result["success"] is False
                assert result["error"] == "Execution timed out."
                assert result["output"] == ""
                assert result["expected_output"] == "expected output"
