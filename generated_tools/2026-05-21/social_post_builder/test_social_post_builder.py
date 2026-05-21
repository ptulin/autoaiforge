import pytest
from unittest.mock import patch, MagicMock
from social_post_builder import generate_post

def test_generate_post_success():
    """Test successful post generation."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Generated post text")]

    with patch("openai.Completion.create", return_value=mock_response):
        result = generate_post("Twitter", "tech enthusiasts", "casual", "new feature release")
        assert result == "Generated post text"

def test_generate_post_failure():
    """Test post generation failure due to API error."""
    with patch("openai.Completion.create", side_effect=Exception("API error")):
        with pytest.raises(RuntimeError, match="Failed to generate post: API error"):
            generate_post("LinkedIn", "B2B", "professional", "launch new product")

def test_generate_post_empty_response():
    """Test post generation with an empty response."""
    mock_response = MagicMock()
    mock_response.choices = []

    with patch("openai.Completion.create", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Failed to generate post: list index out of range"):
            generate_post("Facebook", "general audience", "friendly", "holiday sale")