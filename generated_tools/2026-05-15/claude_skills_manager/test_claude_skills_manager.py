import pytest
from unittest.mock import patch, mock_open
import yaml
from claude_skills_manager import validate_skill_config, load_skill_config, deploy_skill

def test_validate_skill_config():
    valid_config = {
        "name": "Test Skill",
        "description": "A test skill.",
        "triggers": ["trigger1"],
        "actions": ["action1"]
    }
    assert validate_skill_config(valid_config) is True

    invalid_config = {"name": "Test Skill"}
    with pytest.raises(ValueError, match="Missing required key: description"):
        validate_skill_config(invalid_config)

def test_load_skill_config():
    mock_yaml = """
    name: Test Skill
    description: A test skill.
    triggers:
      - trigger1
    actions:
      - action1
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        with patch("os.path.exists", return_value=True):
            config = load_skill_config("fake_path.yaml")
            assert config["name"] == "Test Skill"
            assert config["description"] == "A test skill."

def test_deploy_skill():
    skill_config = {
        "name": "Test Skill",
        "description": "A test skill.",
        "triggers": ["trigger1"],
        "actions": ["action1"]
    }
    mock_response = {"status": "success", "message": "Skill deployed successfully."}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = lambda: None

        result = deploy_skill(skill_config, "http://fake-api.com")
        assert result == mock_response
        mock_post.assert_called_once_with("http://fake-api.com/deploy", json=skill_config)