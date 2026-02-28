import pytest
from unittest.mock import patch, MagicMock
from figma_ai_sync import export_figma_elements, optimize_design_with_ai, update_figma_file

def test_export_figma_elements():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"document": "mock_design_elements"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = export_figma_elements("mock_file_id", "mock_access_token")
        assert result == {"document": "mock_design_elements"}

def test_optimize_design_with_ai():
    with patch("openai.Completion.create") as mock_openai:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="optimized_design_elements")]
        mock_openai.return_value = mock_response

        result = optimize_design_with_ai({"document": "mock_design_elements"}, True)
        assert result == "optimized_design_elements"

def test_update_figma_file():
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        update_figma_file("mock_file_id", "mock_access_token", "optimized_design_elements")
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"] == {"message": "Updated design elements:", "client_meta": "optimized_design_elements"}