import os
import pytest
import requests
from unittest.mock import patch, mock_open
from claude_design_prototype_generator import generate_prototype

def test_generate_prototype_json():
    api_key = "test_api_key"
    prompt = "Create a login page"
    output_format = "json"
    output_file = "output.json"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"mock": "data"}'

    with patch("requests.post", return_value=mock_response) as mock_post:
        with patch("builtins.open", mock_open()) as mock_file:
            result = generate_prototype(api_key, prompt, output_format, output_file)

    mock_post.assert_called_once()
    mock_file.assert_called_once_with(output_file, "wb")
    assert result == output_file

def test_generate_prototype_png():
    api_key = "test_api_key"
    prompt = "Create a dashboard"
    output_format = "png"
    output_file = "output.png"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"binary_image_data"

    with patch("requests.post", return_value=mock_response) as mock_post:
        with patch("builtins.open", mock_open()) as mock_file:
            result = generate_prototype(api_key, prompt, output_format, output_file)

    mock_post.assert_called_once()
    mock_file.assert_called_once_with(output_file, "wb")
    assert result == output_file

def test_generate_prototype_invalid_format():
    api_key = "test_api_key"
    prompt = "Create a profile page"
    output_format = "txt"
    output_file = "output.txt"

    with pytest.raises(ValueError, match="Invalid output format"):
        generate_prototype(api_key, prompt, output_format, output_file)