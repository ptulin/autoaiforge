import pytest
import json
from unittest.mock import patch, MagicMock
from ai_prompt_optimizer import generate_permutations, evaluate_response, optimize_prompts

def test_generate_permutations():
    template = "Explain {{topic}} in {{style}}"
    variables = {"topic": ["AI", "ML"], "style": ["simple", "detailed"]}
    expected_prompts = [
        "Explain AI in simple",
        "Explain AI in detailed",
        "Explain ML in simple",
        "Explain ML in detailed"
    ]
    assert generate_permutations(template, variables) == expected_prompts

def test_evaluate_response():
    response = "This is a test response."
    reference = "This is a test response."
    # Ensure nltk punkt tokenizer is available
    import nltk
    nltk.download('punkt', quiet=True)
    assert evaluate_response(response, reference) > 0.9

def test_optimize_prompts():
    template = "Explain {{topic}} in {{style}}"
    variables = {"topic": ["AI"], "style": ["simple"]}
    reference = "This is a simple explanation of AI."

    with patch("ai_prompt_optimizer.get_ai_response") as mock_get_ai_response:
        mock_get_ai_response.return_value = "This is a simple explanation of AI."
        results = optimize_prompts(template, variables, reference, "gpt-5", "fake-api-key")

    assert len(results) == 1
    assert results[0]["prompt"] == "Explain AI in simple"
    assert results[0]["response"] == "This is a simple explanation of AI."
    assert results[0]["score"] > 0.9
