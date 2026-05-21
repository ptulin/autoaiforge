import pytest
from unittest.mock import patch
from multi_agent_code_refactor import refactor_code

def test_refactor_code_with_mocked_agents():
    with patch("multi_agent_code_refactor.CodeRefactorAgent.review_code") as mock_review_code:
        mock_review_code.side_effect = [
            "# Refactored by style agent\ndef foo():\n    pass",
            "# Refactored by performance agent\ndef foo():\n    pass",
            "# Refactored by security agent\ndef foo():\n    pass",
        ]

        input_code = "def foo():\n    pass"
        agents = ["style", "performance", "security"]

        refactored_code, report = refactor_code(input_code, agents)

        assert "# Refactored by security agent" in refactored_code
        assert "Agent (style):" in report
        assert "Agent (performance):" in report
        assert "Agent (security):" in report

def test_refactor_code_with_file_input(tmp_path):
    input_file = tmp_path / "input.py"
    input_file.write_text("def foo():\n    pass")

    with patch("multi_agent_code_refactor.CodeRefactorAgent.review_code") as mock_review_code:
        mock_review_code.return_value = "# Refactored code\ndef foo():\n    pass"

        refactored_code, report = refactor_code(str(input_file), ["style"])

        assert "# Refactored code" in refactored_code
        assert "Agent (style):" in report

def test_refactor_code_with_output_file(tmp_path):
    input_code = "def foo():\n    pass"
    output_file = tmp_path / "output.py"

    with patch("multi_agent_code_refactor.CodeRefactorAgent.review_code") as mock_review_code:
        mock_review_code.return_value = "# Refactored code\ndef foo():\n    pass"

        refactor_code(input_code, ["style"], output_file=str(output_file))

        assert output_file.read_text() == "# Refactored code\ndef foo():\n    pass"