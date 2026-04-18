import os
import pytest
import requests
from unittest.mock import patch, MagicMock
from claude_ui_blueprinter import generate_blueprint

def mock_post_success(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.json.return_value = {"html": "<h1>Generated UI</h1>"}
    mock_response.raise_for_status = MagicMock()
    return mock_response

def mock_post_failure(*args, **kwargs):
    raise requests.RequestException("API failure")

def test_generate_flask_blueprint_success(tmp_path):
    with patch('requests.post', side_effect=mock_post_success):
        output_dir = tmp_path / "flask_blueprint"
        generate_blueprint('flask', 'dark', 'grid', str(output_dir))
        assert (output_dir / 'ui_blueprint.py').exists()
        with open(output_dir / 'ui_blueprint.py') as f:
            content = f.read()
            assert "<h1>Generated UI</h1>" in content

def test_generate_django_blueprint_success(tmp_path):
    with patch('requests.post', side_effect=mock_post_success):
        output_dir = tmp_path / "django_blueprint"
        generate_blueprint('django', 'light', 'list', str(output_dir))
        assert (output_dir / 'views.py').exists()
        assert (output_dir / 'urls.py').exists()
        with open(output_dir / 'views.py') as f:
            content = f.read()
            assert "<h1>Generated UI</h1>" in content

def test_generate_blueprint_api_failure():
    with patch('requests.post', side_effect=mock_post_failure):
        with pytest.raises(RuntimeError, match="Failed to fetch UI components from Claude Design API"):
            generate_blueprint('flask', 'dark', 'grid', '/tmp')