import pytest
from unittest.mock import patch, MagicMock
from llm_prompt_optimizer import generate_prompt_variations, evaluate_prompts, find_best_prompt

def mock_scoring_function(prompt, response):
    return len(response)  # Example scoring: longer responses get higher scores

def test_generate_prompt_variations():
    base_prompt = "Translate to French:"
    variations = generate_prompt_variations(base_prompt, num_variations=3)
    assert len(variations) == 3
    assert variations[0] == "Translate to French: (variation 1)"

def test_evaluate_prompts():
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [{"generated_text": "Bonjour"}]

    with patch("llm_prompt_optimizer.pipeline", return_value=mock_pipeline):
        prompts = ["Translate to French: Hello"]
        results = evaluate_prompts(prompts, "mock-model", mock_scoring_function)

    assert len(results) == 1
    assert results[0]["prompt"] == "Translate to French: Hello"
    assert results[0]["response"] == "Bonjour"
    assert results[0]["score"] == len("Bonjour")

def test_find_best_prompt():
    results = [
        {"prompt": "Prompt 1", "response": "Response 1", "score": 10},
        {"prompt": "Prompt 2", "response": "Response 2", "score": 20},
        {"prompt": "Prompt 3", "response": "Response 3", "score": 15},
    ]
    best_prompt = find_best_prompt(results)
    assert best_prompt["prompt"] == "Prompt 2"
    assert best_prompt["score"] == 20