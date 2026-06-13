import pytest
from unittest.mock import patch
from policy_enforcer import PolicyEnforcer

def test_valid_policy_and_action():
    rules = [
        {
            "name": "Limit action type",
            "condition": {"type": {"allowed": ["read", "write"]}},
            "message": "Action type not allowed"
        }
    ]

    action = {"type": "read"}
    enforcer = PolicyEnforcer(rules)
    result = enforcer.check(action)

    assert result["compliant"] is True
    assert result["violations"] == []

def test_policy_violation():
    rules = [
        {
            "name": "Limit action type",
            "condition": {"type": {"allowed": ["read", "write"]}},
            "message": "Action type not allowed"
        }
    ]

    action = {"type": "delete"}
    enforcer = PolicyEnforcer(rules)
    result = enforcer.check(action)

    assert result["compliant"] is False
    assert len(result["violations"]) == 1
    assert result["violations"][0]["rule"] == "Limit action type"

def test_invalid_rule_format():
    rules = [
        {
            "name": "Invalid Rule",
            "condition": "not a dict",
            "message": "This rule is invalid"
        }
    ]

    with pytest.raises(ValueError):
        PolicyEnforcer(rules)
