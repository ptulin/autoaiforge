import pytest
from unittest.mock import patch, mock_open, MagicMock
from prompt_optimizer import load_test_cases, load_scorer, generate_prompt_variations, evaluate_prompts

def test_load_test_cases():
    mock_data = '[{"text": "hello"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        test_cases = load_test_cases("test_cases.json")
        assert test_cases == [{"text": "hello"}]

def test_load_scorer():
    mock_scorer = MagicMock()
    mock_scorer.score = lambda x, y: 1

    with patch("importlib.util.spec_from_file_location") as mock_spec:
        mock_loader = MagicMock()
        mock_loader.exec_module = lambda module: setattr(module, "score", mock_scorer.score)
        mock_spec.return_value.loader = mock_loader
        scorer = load_scorer("scorer.py")
        assert scorer({"text": "test"}, "output") == 1

def test_generate_prompt_variations():
    base_prompt = "Translate {text} to {language}"
    placeholders = {
        "text": ["hello", "world"],
        "language": ["French", "Spanish"]
    }
    variations = generate_prompt_variations(base_prompt, placeholders)
    expected = [
        "Translate hello to French",
        "Translate hello to Spanish",
        "Translate world to French",
        "Translate world to Spanish"
    ]
    assert sorted(variations) == sorted(expected)

def test_evaluate_prompts():
    prompts = ["Translate {text} to French"]
    test_cases = [{"text": "hello"}, {"text": "world"}]
    mock_scorer = lambda tc, output: len(output)

    with patch("prompt_optimizer.query_llm", return_value="Bonjour"):
        results = evaluate_prompts(prompts, test_cases, mock_scorer)
        assert results[0]["average_score"] == 7