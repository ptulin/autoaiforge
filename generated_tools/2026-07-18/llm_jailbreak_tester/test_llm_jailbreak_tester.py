import pytest
from unittest.mock import patch, MagicMock
import llm_jailbreak_tester

def test_load_prompts(tmp_path):
    prompts_file = tmp_path / "prompts.json"
    prompts_file.write_text('["Test prompt 1", "Test prompt 2"]')
    prompts = llm_jailbreak_tester.load_prompts(prompts_file)
    assert prompts == ["Test prompt 1", "Test prompt 2"]

def test_load_prompts_file_not_found():
    with pytest.raises(FileNotFoundError):
        llm_jailbreak_tester.load_prompts("nonexistent.json")

@patch("openai.Completion.create")
def test_evaluate_prompt(mock_create):
    mock_create.return_value = {"choices": [{"text": "This is a safe response."}]}
    response = llm_jailbreak_tester.evaluate_prompt("fake_api_key", "Test prompt")
    assert response == "This is a safe response."

@patch("openai.Completion.create")
def test_test_prompts(mock_create):
    mock_create.return_value = {"choices": [{"text": "This is a safe response."}]}
    prompts = ["Test prompt"]
    results = llm_jailbreak_tester.test_prompts("fake_api_key", prompts)
    assert len(results) == 1
    assert results[0]["prompt"] == "Test prompt"
    assert results[0]["passed"] is True

@patch("openai.Completion.create")
def test_test_prompts_fail(mock_create):
    mock_create.return_value = {"choices": [{"text": "[JAILBREAK]"}]}
    prompts = ["Test prompt"]
    results = llm_jailbreak_tester.test_prompts("fake_api_key", prompts)
    assert len(results) == 1
    assert results[0]["prompt"] == "Test prompt"
    assert results[0]["passed"] is False