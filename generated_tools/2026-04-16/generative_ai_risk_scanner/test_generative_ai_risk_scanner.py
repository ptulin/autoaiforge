import pytest
import json
from unittest.mock import patch, MagicMock
from generative_ai_risk_scanner import analyze_model_parameters, simulate_prompt_injection, main

def test_analyze_model_parameters():
    config = {"temperature": 0.4, "top_p": 0.95}
    risks = analyze_model_parameters(config)
    assert len(risks) == 2
    assert "Temperature is too low" in risks[0]
    assert "Top-p value is too high" in risks[1]

@patch("generative_ai_risk_scanner.MagicMock")
def test_simulate_prompt_injection(mock_model):
    mock_tokenizer = MagicMock()
    mock_tokenizer.decode.side_effect = ["malicious content", "benign content"]

    mock_model.generate.side_effect = [["malicious content"], ["benign content"]]

    result = simulate_prompt_injection("test-model", mock_tokenizer)
    assert result == "Model is vulnerable to prompt injection attacks."

    result = simulate_prompt_injection("test-model", mock_tokenizer)
    assert result == "Model is not vulnerable to prompt injection attacks."

@patch("generative_ai_risk_scanner.open")
def test_main_with_config(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({"temperature": 0.4, "top_p": 0.95})
    mock_open.return_value.__enter__.return_value.write = MagicMock()

    with patch("builtins.print") as mock_print:
        with patch("generative_ai_risk_scanner.os.path.exists", return_value=True):
            main(["--model-id", "test-model", "--config-file", "test.json", "--output", "report.json"])
            mock_print.assert_called_with("Vulnerability report saved to report.json")
