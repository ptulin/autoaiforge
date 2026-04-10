import pytest
from unittest.mock import patch
from prompt_debugger import analyze_prompt

def mock_openai_chatcompletion_create(model, messages):
    """Mock function to simulate OpenAI API responses."""
    responses = {
        "Write a story about a dragon. (in a humorous tone)": "This is a humorous response.",
        "Write a story about a dragon. (in one sentence)": "This is a one-sentence response.",
        "Write a story about a dragon. (with a twist ending)": "This is a response with a twist ending.",
        "Write a story about a dragon. (as a poem)": "This is a poetic response.",
        "Write a story about a dragon. (in the style of Shakespeare)": "This is a Shakespearean response."
    }

    case = messages[0]['content']
    return {
        "choices": [
            {"message": {"content": responses.get(case, "Error: Unknown case.")}}
        ]
    }

@patch("openai.ChatCompletion.create", side_effect=mock_openai_chatcompletion_create)
def test_analyze_prompt(mock_create):
    prompt = "Write a story about a dragon."
    model = "gpt-3.5-turbo"

    report = analyze_prompt(prompt, model)

    assert "Prompt Diagnostic Report:" in report
    assert "Edge case 'Write a story about a dragon. (in a humorous tone)' produced a valid response." in report
    assert "Edge case 'Write a story about a dragon. (in one sentence)' produced a valid response." in report

@patch("openai.ChatCompletion.create")
def test_analyze_prompt_empty_response(mock_create):
    def mock_empty_response(model, messages):
        return {"choices": [{"message": {"content": ""}}]}

    mock_create.side_effect = mock_empty_response

    prompt = "Write a story about a dragon."
    model = "gpt-3.5-turbo"

    report = analyze_prompt(prompt, model)

    assert "produced an empty response" in report

@patch("openai.ChatCompletion.create")
def test_analyze_prompt_error_response(mock_create):
    def mock_error_response(model, messages):
        return {"choices": [{"message": {"content": "Error: Something went wrong."}}]}

    mock_create.side_effect = mock_error_response

    prompt = "Write a story about a dragon."
    model = "gpt-3.5-turbo"

    report = analyze_prompt(prompt, model)

    assert "resulted in an error-like response" in report
