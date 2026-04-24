import pytest
from unittest.mock import patch, MagicMock
import code_to_diagram_converter

def test_generate_diagram_from_code_success():
    code = "def add(a, b):\n    return a + b"
    output_format = "png"
    api_key = "test_api_key"

    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "start -> add\nadd -> end"
                }
            }
        ]
    }

    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with patch("graphviz.Digraph.render", return_value="diagram.png") as mock_render:
            output_file = code_to_diagram_converter.generate_diagram_from_code(code, output_format, api_key)
            assert output_file == "diagram.png"
            mock_render.assert_called_once()

def test_generate_diagram_from_code_invalid_format():
    code = "def add(a, b):\n    return a + b"
    output_format = "invalid_format"
    api_key = "test_api_key"

    with pytest.raises(ValueError, match="Invalid output format. Supported formats are: png, svg, dot."):
        code_to_diagram_converter.generate_diagram_from_code(code, output_format, api_key)

def test_generate_diagram_from_code_api_error():
    code = "def add(a, b):\n    return a + b"
    output_format = "png"
    api_key = "test_api_key"

    with patch("openai.ChatCompletion.create", side_effect=Exception("API Error")):
        with pytest.raises(RuntimeError, match="Error generating diagram description: API Error"):
            code_to_diagram_converter.generate_diagram_from_code(code, output_format, api_key)

def test_generate_diagram_from_code_empty_response():
    code = "def add(a, b):\n    return a + b"
    output_format = "png"
    api_key = "test_api_key"

    mock_response = {
        'choices': [
            {
                'message': {
                    'content': ""
                }
            }
        ]
    }

    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Error generating diagram description: Empty response from OpenAI API"):
            code_to_diagram_converter.generate_diagram_from_code(code, output_format, api_key)

def test_generate_diagram_from_code_invalid_code():
    code = ""
    output_format = "png"
    api_key = "test_api_key"

    with pytest.raises(ValueError, match="Code input cannot be empty."):
        code_to_diagram_converter.generate_diagram_from_code(code, output_format, api_key)
