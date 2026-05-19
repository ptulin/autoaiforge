import pytest
import json
from unittest.mock import patch, MagicMock
from recursive_token_profiler import profile_token_usage, visualize_token_growth

def test_profile_token_usage_valid_config(tmp_path):
    config = {
        "model": "gpt-3.5-turbo",
        "task": "Simulate recursive reasoning task.",
        "max_depth": 3,
        "token_limit": 1000
    }
    config_path = tmp_path / "config.json"
    output_path = tmp_path / "output.json"

    with open(config_path, 'w') as f:
        json.dump(config, f)

    result = profile_token_usage(config_path, output_path)

    assert "depth" in result
    assert "tokens" in result
    assert output_path.exists()

def test_profile_token_usage_missing_task(tmp_path):
    config = {
        "model": "gpt-3.5-turbo",
        "max_depth": 3,
        "token_limit": 1000
    }
    config_path = tmp_path / "config.json"
    output_path = tmp_path / "output.json"

    with open(config_path, 'w') as f:
        json.dump(config, f)

    with pytest.raises(ValueError, match="Task description is missing"):
        profile_token_usage(config_path, output_path)

@patch("recursive_token_profiler.encoding_for_model")
def test_profile_token_usage_mocked_encoding(mock_encoding, tmp_path):
    mock_encoding.return_value = MagicMock(encode=lambda x: [1, 2, 3])

    config = {
        "model": "gpt-3.5-turbo",
        "task": "Mocked task.",
        "max_depth": 2,
        "token_limit": 1000
    }
    config_path = tmp_path / "config.json"
    output_path = tmp_path / "output.json"

    with open(config_path, 'w') as f:
        json.dump(config, f)

    result = profile_token_usage(config_path, output_path)

    assert result["depth"] == 1
    assert result["tokens"] > 0
    assert output_path.exists()