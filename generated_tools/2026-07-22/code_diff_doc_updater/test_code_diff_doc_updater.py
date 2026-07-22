import pytest
from unittest.mock import patch, MagicMock
from code_diff_doc_updater import analyze_git_diff, generate_docstring, update_documentation

def test_analyze_git_diff():
    with patch('code_diff_doc_updater.Repo') as mock_repo:
        mock_repo.return_value.git.diff.return_value = "mock_diff"
        diff = analyze_git_diff("/mock/repo", branch="main")
        assert diff == "mock_diff"

def test_generate_docstring():
    with patch('code_diff_doc_updater.openai.Completion.create') as mock_openai:
        mock_openai.return_value.choices = [MagicMock(text="Generated docstring")]
        docstring = generate_docstring("mock_diff", "mock_api_key")
        assert docstring == "Generated docstring"

def test_update_documentation(tmp_path):
    readme_path = tmp_path / "README.md"
    readme_path.write_text("# Project\n")
    update_documentation(str(tmp_path), "New docstring")
    updated_content = readme_path.read_text()
    assert "New docstring" in updated_content
