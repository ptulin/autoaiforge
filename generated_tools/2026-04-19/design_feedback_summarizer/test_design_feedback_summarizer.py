import pytest
import json
from unittest.mock import patch
from design_feedback_summarizer import summarize_feedback

def test_summarize_feedback_json_input(tmp_path):
    input_data = ["Great design!", "Navigation is confusing.", "Add more color themes."]
    input_file = tmp_path / "feedback.json"
    output_file = tmp_path / "output.json"

    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(input_data, f)

    with patch("design_feedback_summarizer.call_claude_api") as mock_api:
        mock_api.return_value = {
            "summary": "Users appreciate the clean design but find navigation confusing.",
            "recommendations": [
                "Improve navigation clarity by adding labels to icons.",
                "Provide a tutorial for first-time users."
            ]
        }
        result = summarize_feedback(str(input_file), str(output_file), "json")

    assert result["summary"] == "Users appreciate the clean design but find navigation confusing."
    assert "Improve navigation clarity" in result["recommendations"][0]


def test_summarize_feedback_text_input(tmp_path):
    input_data = "Great design!\nNavigation is confusing.\nAdd more color themes."
    input_file = tmp_path / "feedback.txt"
    output_file = tmp_path / "output.txt"

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(input_data)

    with patch("design_feedback_summarizer.call_claude_api") as mock_api:
        mock_api.return_value = {
            "summary": "Users appreciate the clean design but find navigation confusing.",
            "recommendations": [
                "Improve navigation clarity by adding labels to icons.",
                "Provide a tutorial for first-time users."
            ]
        }
        result = summarize_feedback(str(input_file), str(output_file), "text")

    assert result["summary"] == "Users appreciate the clean design but find navigation confusing."
    assert "Improve navigation clarity" in result["recommendations"][0]


def test_invalid_file_format(tmp_path):
    input_file = tmp_path / "feedback.csv"
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("Invalid format")

    with pytest.raises(ValueError, match="Unsupported file format"):
        summarize_feedback(str(input_file))
