import pytest
import json
from unittest.mock import patch, mock_open
from ux_audit_generator import fetch_audit_results, generate_report

def test_fetch_audit_results():
    api_url = "https://api.claude.design/audit"
    api_key = "test_api_key"
    prototype_data = {"mock": "data"}
    description = "Test prototype"

    mock_response = {"summary": "Test summary", "issues": [{"title": "Issue 1", "description": "Description 1"}]}

    with patch("ux_audit_generator.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = fetch_audit_results(api_url, api_key, prototype_data, description)

        assert result == mock_response
        mock_post.assert_called_once_with(
            api_url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"prototype_data": prototype_data, "description": description}
        )

def test_generate_report_md():
    audit_results = {
        "summary": "Test summary",
        "issues": [
            {"title": "Issue 1", "description": "Description 1"},
            {"title": "Issue 2", "description": "Description 2"}
        ]
    }

    result = generate_report(audit_results, "md")

    assert "# UX Audit Report" in result
    assert "## Summary" in result
    assert "Test summary" in result
    assert "- **Issue 1**: Description 1" in result
    assert "- **Issue 2**: Description 2" in result

def test_generate_report_html():
    audit_results = {
        "summary": "Test summary",
        "issues": [
            {"title": "Issue 1", "description": "Description 1"},
            {"title": "Issue 2", "description": "Description 2"}
        ]
    }

    result = generate_report(audit_results, "html")

    assert "<html>" in result
    assert "<h1>UX Audit Report</h1>" in result
    assert "<p>Test summary</p>" in result
    assert "<li><strong>Issue 1</strong>: Description 1</li>" in result
    assert "<li><strong>Issue 2</strong>: Description 2</li>" in result