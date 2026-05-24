import pytest
import json
from unittest.mock import patch, mock_open
from ai_dependency_audit import audit_dependencies, parse_dependencies, analyze_dependency

def test_parse_dependencies_requirements():
    content = """requests==2.25.1
    flask>=2.0.0
    numpy==1.21.0
    """
    file_path = "requirements.txt"
    expected = [
        {"name": "requests", "version": "2.25.1"},
        {"name": "flask", "version": "2.0.0"},
        {"name": "numpy", "version": "1.21.0"}
    ]
    result = parse_dependencies(file_path, content)
    assert result == expected

def test_parse_dependencies_package_json():
    content = json.dumps({
        "dependencies": {
            "express": "4.17.1",
            "lodash": "4.17.21"
        }
    })
    file_path = "package.json"
    expected = [
        {"name": "express", "version": "4.17.1"},
        {"name": "lodash", "version": "4.17.21"}
    ]
    result = parse_dependencies(file_path, content)
    assert result == expected

def test_audit_dependencies():
    file_content = "requests==2.25.1\nflask>=2.0.0\nnumpy==1.21.0"
    file_path = "requirements.txt"

    mock_response = [
        {
            "package": "requests",
            "current_version": "2.25.1",
            "latest_version": "2.26.0",
            "risk_level": "moderate",
            "safer_alternatives": ["requests==2.26.0"]
        }
    ]

    with patch("builtins.open", mock_open(read_data=file_content)):
        with patch("ai_dependency_audit.analyze_dependency") as mock_analyze:
            mock_analyze.side_effect = [
                ("2.26.0", "moderate", ["requests==2.26.0"]),
                ("2.1.0", "safe", []),
                ("1.21.0", "safe", [])
            ]
            result = audit_dependencies(file_path)

    assert result == mock_response
