import pytest
from unittest.mock import patch, mock_open
from code_review_simulator import load_file, validate_agent_feedback, evaluate_feedback
import json
import yaml

@pytest.fixture
def mock_pr_template():
    return {
        "issues": [
            {"id": "1", "expected_feedback": "Fix the off-by-one error."},
            {"id": "2", "expected_feedback": "Add input validation."}
        ]
    }

@pytest.fixture
def mock_agent_feedback():
    return {
        "feedback": {
            "1": "Fix the off-by-one error.",
            "2": "Add input validation."
        }
    }

@pytest.fixture
def mock_schema():
    return {
        "type": "object",
        "properties": {
            "feedback": {
                "type": "object",
                "patternProperties": {
                    "^\\d+$": {"type": "string"}
                }
            }
        },
        "required": ["feedback"]
    }

def test_load_file_json():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_file("test.json")
        assert result == {"key": "value"}

def test_load_file_yaml():
    mock_data = "key: value"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_file("test.yaml")
        assert result == {"key": "value"}

def test_evaluate_feedback(mock_pr_template, mock_agent_feedback):
    results = evaluate_feedback(mock_pr_template, mock_agent_feedback)
    assert results["score"] == 2
    assert results["max_score"] == 2
    assert len(results["details"]) == 2
    assert results["details"][0]["result"] == "correct"
    assert results["details"][1]["result"] == "correct"

def test_validate_agent_feedback(mock_agent_feedback, mock_schema):
    # Should not raise an exception
    validate_agent_feedback(mock_agent_feedback, mock_schema)

def test_validate_agent_feedback_invalid(mock_schema):
    invalid_feedback = {"invalid_key": "value"}
    with pytest.raises(Exception):
        validate_agent_feedback(invalid_feedback, mock_schema)
