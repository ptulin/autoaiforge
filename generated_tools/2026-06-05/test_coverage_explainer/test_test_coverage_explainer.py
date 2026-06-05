import pytest
from unittest.mock import patch, mock_open
import os
from test_coverage_explainer import analyze_coverage, generate_ai_suggestions

def test_analyze_coverage():
    mock_report = """
    <coverage>
        <packages>
            <package>
                <classes>
                    <class filename="test_file.py">
                        <lines>
                            <line number="10" hits="0"/>
                            <line number="20" hits="1"/>
                            <line number="30" hits="0"/>
                        </lines>
                    </class>
                </classes>
            </package>
        </packages>
    </coverage>
    """

    with patch("builtins.open", mock_open(read_data=mock_report)):
        with patch("os.path.exists", return_value=True):
            uncovered = analyze_coverage("fake_path.xml")

    assert uncovered == {"test_file.py": [10, 30]}

def test_analyze_coverage_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            analyze_coverage("non_existent_file.xml")

def test_generate_ai_suggestions():
    uncovered = {"test_file.py": [10, 30]}

    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = {"choices": [{"text": "Add tests for edge cases."}]}
        suggestions = generate_ai_suggestions(uncovered)

    assert "test_file.py" in suggestions
    assert "Add tests for edge cases." in suggestions["test_file.py"]

def test_generate_ai_suggestions_api_error():
    uncovered = {"test_file.py": [10, 30]}

    with patch("openai.Completion.create", side_effect=Exception("API error")):
        suggestions = generate_ai_suggestions(uncovered)

    assert "test_file.py" in suggestions
    assert suggestions["test_file.py"].startswith("Error generating suggestion")