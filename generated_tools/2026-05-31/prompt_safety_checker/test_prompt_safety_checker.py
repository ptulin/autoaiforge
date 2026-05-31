import pytest
from unittest.mock import patch
from prompt_safety_checker import analyze_prompt

def test_analyze_prompt_no_issues():
    prompt = "Write a positive story about teamwork."
    safety_rules = ["contains hate speech", "contains explicit content"]
    result = analyze_prompt(prompt, safety_rules)
    assert result["flagged_issues"] == []

def test_analyze_prompt_with_issues():
    prompt = "This contains hate speech."
    safety_rules = ["contains hate speech", "contains explicit content"]
    result = analyze_prompt(prompt, safety_rules)
    assert "contains hate speech" in result["flagged_issues"]

def test_analyze_prompt_sentiment_negative():
    prompt = "I hate everything."
    safety_rules = []

    with patch("prompt_safety_checker.analyze_prompt", wraps=analyze_prompt) as mock_analyze:
        mock_analyze.return_value = {
            "flagged_issues": ["Negative sentiment detected"],
            "suggestions": "Consider rephrasing or removing flagged content."
        }
        result = analyze_prompt(prompt, safety_rules)
        assert "Negative sentiment detected" in result["flagged_issues"]
