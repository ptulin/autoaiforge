import pytest
from unittest.mock import patch, MagicMock
from code_change_summarizer import summarize_diff, get_commit_diffs, generate_summaries

def test_summarize_diff():
    with patch("openai.ChatCompletion.create") as mock_openai:
        mock_openai.return_value = {
            'choices': [{'message': {'content': 'This is a summary of the changes.'}}]
        }
        diff_text = "- old line\n+ new line"
        summary = summarize_diff(diff_text)
        assert summary == "This is a summary of the changes."

def test_get_commit_diffs():
    with patch("code_change_summarizer.Repo") as mock_repo:
        mock_repo.return_value.git.log.return_value = "commit1\ncommit2"
        mock_commit = MagicMock()
        mock_commit.diff.return_value = [MagicMock(diff=b"- old line\n+ new line")]
        mock_repo.return_value.commit.return_value = mock_commit

        diffs = get_commit_diffs("/fake/repo", "HEAD~2..HEAD")
        assert len(diffs) == 2
        assert len(diffs[0]) == 1

def test_generate_summaries():
    with patch("code_change_summarizer.get_commit_diffs") as mock_get_diffs, \
         patch("code_change_summarizer.summarize_diff") as mock_summarize_diff:

        mock_get_diffs.return_value = [[MagicMock(diff=b"- old line\n+ new line")]]
        mock_summarize_diff.return_value = "This is a summary of the changes."

        summaries = generate_summaries("/fake/repo", "HEAD~1..HEAD", "text")
        assert "This is a summary of the changes." in summaries