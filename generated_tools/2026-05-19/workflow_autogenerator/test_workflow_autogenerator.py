import pytest
from unittest.mock import patch, MagicMock
from workflow_autogenerator import generate_workflow

@patch('openai.Completion.create')
def test_generate_workflow_valid(mock_openai):
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="name: Test Workflow\njobs:\n  build:\n    runs-on: ubuntu-latest\n")])

    prompt = "Build and test a Python package on push events"
    platform = "github"
    api_key = "test_api_key"

    result = generate_workflow(prompt, platform, api_key)

    assert "name: Test Workflow" in result
    assert "jobs:" in result
    assert "build:" in result

@patch('openai.Completion.create')
def test_generate_workflow_invalid_yaml(mock_openai):
    mock_openai.return_value = MagicMock(choices=[MagicMock(text="invalid: [unclosed")])

    prompt = "Build and test a Python package on push events"
    platform = "github"
    api_key = "test_api_key"

    with pytest.raises(ValueError, match="Generated YAML is invalid."):
        generate_workflow(prompt, platform, api_key)

@patch('openai.Completion.create')
def test_generate_workflow_unsupported_platform(mock_openai):
    prompt = "Build and test a Python package on push events"
    platform = "unsupported_platform"
    api_key = "test_api_key"

    with pytest.raises(ValueError, match="Unsupported platform"):
        generate_workflow(prompt, platform, api_key)