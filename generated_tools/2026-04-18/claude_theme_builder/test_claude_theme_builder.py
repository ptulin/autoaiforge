import pytest
import json
from unittest.mock import patch, mock_open
from claude_theme_builder import ThemeBuilder, fetch_design_defaults, load_config

def test_theme_builder_generate_css():
    config = {"primary_color": "#ff0000", "font_family": "Arial"}
    framework = "bootstrap"
    builder = ThemeBuilder(config, framework)

    with patch("claude_theme_builder.Environment.get_template") as mock_get_template:
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "/* Generated CSS */"

        css = builder.generate_css()
        assert css == "/* Generated CSS */"
        mock_get_template.assert_called_once_with("bootstrap.css.j2")
        mock_template.render.assert_called_once_with(config)

def test_fetch_design_defaults():
    mock_response = {"primary_color": "#000000", "font_family": "Helvetica"}

    with patch("claude_theme_builder.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None

        defaults = fetch_design_defaults()
        assert defaults == mock_response
        mock_get.assert_called_once_with("https://api.claude.design/defaults", timeout=10)

def test_load_config():
    mock_config = {"primary_color": "#123456", "font_family": "Verdana"}
    mock_file_content = json.dumps(mock_config)

    with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
        config = load_config("mock_config.json")
        assert config == mock_config
        mock_file.assert_called_once_with("mock_config.json", 'r')