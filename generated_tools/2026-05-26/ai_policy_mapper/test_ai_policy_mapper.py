import pytest
from unittest.mock import patch, mock_open
from ai_policy_mapper import PolicyMapper
import json
import yaml
from jsonschema.exceptions import ValidationError

def test_load_policy_valid():
    policy_yaml = """
    schema:
      type: object
      properties:
        name:
          type: string
        age:
          type: integer
      required: [name, age]
    """
    with patch("builtins.open", mock_open(read_data=policy_yaml)):
        policy = PolicyMapper.load_policy("policy.yaml")
        assert "schema" in policy
        assert policy["schema"]["type"] == "object"

def test_load_policy_invalid_yaml():
    invalid_yaml = "schema: [type: object"
    with patch("builtins.open", mock_open(read_data=invalid_yaml)):
        with pytest.raises(ValueError, match="Error parsing YAML file"):
            PolicyMapper.load_policy("policy.yaml")

def test_match_features_to_policies_compliant():
    policy_yaml = """
    schema:
      type: object
      properties:
        name:
          type: string
        age:
          type: integer
      required: [name, age]
    """
    features = {"name": "AI Model", "age": 5}

    with patch("builtins.open", mock_open(read_data=policy_yaml)):
        gaps = PolicyMapper.match_features_to_policies(features, "policy.yaml")
        assert gaps == []

def test_match_features_to_policies_non_compliant():
    policy_yaml = """
    schema:
      type: object
      properties:
        name:
          type: string
        age:
          type: integer
      required: [name, age]
    """
    features = {"name": "AI Model"}  # Missing 'age'

    with patch("builtins.open", mock_open(read_data=policy_yaml)):
        gaps = PolicyMapper.match_features_to_policies(features, "policy.yaml")
        assert len(gaps) == 1
        assert "'age' is a required property" in gaps[0]

def test_match_features_to_policies_invalid_policy():
    invalid_policy_yaml = "schema: {}"
    features = {"name": "AI Model", "age": 5}

    with patch("builtins.open", mock_open(read_data=invalid_policy_yaml)):
        gaps = PolicyMapper.match_features_to_policies(features, "policy.yaml")
        assert len(gaps) == 1
        assert "Policy file does not contain a valid schema." in gaps[0]