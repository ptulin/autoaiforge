import pytest
from unittest.mock import patch, Mock
from llm_ci_test_automation import fetch_pr_diff, generate_test_cases

def test_fetch_pr_diff_success():
    with patch("llm_ci_test_automation.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"diff_url": "https://example.com/diff"}
        mock_get.return_value = mock_response

        mock_diff_response = Mock()
        mock_diff_response.status_code = 200
        mock_diff_response.text = "diff content"
        mock_get.side_effect = [mock_response, mock_diff_response]

        diff = fetch_pr_diff("github.com/user/repo", 42, "fake_token")
        assert diff == "diff content"

def test_fetch_pr_diff_failure():
    with patch("llm_ci_test_automation.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Failed to fetch PR diff: 404, Not Found"):
            fetch_pr_diff("github.com/user/repo", 42, "fake_token")

def test_generate_test_cases_success():
    with patch("llm_ci_test_automation.fetch_pr_diff") as mock_fetch_diff, \
         patch("llm_ci_test_automation.openai.Completion.create") as mock_openai_create:

        mock_fetch_diff.return_value = "mock diff"
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock(text="[{'name': 'test_case_1', 'code': 'assert 1 == 1'}]")]
        mock_openai_create.return_value = mock_openai_response

        test_cases = generate_test_cases("github.com/user/repo", 42, "fake_token", "fake_openai_key")
        assert test_cases == [{'name': 'test_case_1', 'code': 'assert 1 == 1'}]

def test_generate_test_cases_invalid_response():
    with patch("llm_ci_test_automation.fetch_pr_diff") as mock_fetch_diff, \
         patch("llm_ci_test_automation.openai.Completion.create") as mock_openai_create:

        mock_fetch_diff.return_value = "mock diff"
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock(text="invalid response")]
        mock_openai_create.return_value = mock_openai_response

        with pytest.raises(RuntimeError, match="Failed to parse generated test cases."):
            generate_test_cases("github.com/user/repo", 42, "fake_token", "fake_openai_key")