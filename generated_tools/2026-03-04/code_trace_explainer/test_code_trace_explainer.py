import pytest
import json
from unittest.mock import patch, MagicMock
from code_trace_explainer import analyze_trace, generate_ai_insights

def test_analyze_trace():
    trace_data = {
        "trace": [
            {
                "function": "my_function",
                "line": 10,
                "variables": {"x": 5, "y": 10}
            },
            {
                "function": "another_function",
                "line": 20,
                "variables": {"z": 15}
            }
        ]
    }
    expected_output = (
        "Function: my_function, Line: 10\n"
        "Variables:\n"
        "  x: 5\n"
        "  y: 10\n\n"
        "Function: another_function, Line: 20\n"
        "Variables:\n"
        "  z: 15"
    )
    assert analyze_trace(trace_data) == expected_output

@patch("openai.Completion.create")
def test_generate_ai_insights(mock_openai):
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="AI Insight Example")])
    trace_analysis = "Function: my_function, Line: 10\nVariables:\n  x: 5\n  y: 10"
    result = generate_ai_insights(trace_analysis)
    assert result == "AI Insight Example"

@patch("openai.Completion.create")
def test_generate_ai_insights_error(mock_openai):
    mock_openai.side_effect = Exception("API Error")
    trace_analysis = "Function: my_function, Line: 10\nVariables:\n  x: 5\n  y: 10"
    result = generate_ai_insights(trace_analysis)
    assert result == "Error generating AI insights: API Error"