import pytest
from unittest.mock import patch, MagicMock
from claude_ui_customizer import fetch_design, modify_design, update_design, Design, ClaudeAPIError

API_URL = "http://mockapi.com"
DESIGN_ID = "12345"

@pytest.fixture
def mock_design():
    return Design(id=DESIGN_ID, layout={"theme": "light", "dimensions": {"width": 1280, "height": 720}})

def test_fetch_design(mock_design):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_design.dict()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        design = fetch_design(API_URL, DESIGN_ID)
        assert design.id == mock_design.id
        assert design.layout == mock_design.layout

def test_modify_design(mock_design):
    modified = modify_design(mock_design, theme="dark", resize=(1920, 1080))
    assert modified.layout["theme"] == "dark"
    assert modified.layout["dimensions"] == {"width": 1920, "height": 1080}

def test_update_design(mock_design):
    with patch("requests.put") as mock_put:
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_put.return_value = mock_response

        update_design(API_URL, mock_design)
        mock_put.assert_called_once_with(f"{API_URL}/designs/{mock_design.id}", json=mock_design.dict())