import pytest
import json
from unittest.mock import patch
from gpt_dynamic_toolchain import validate_toolchain_schema, execute_toolchain

def test_validate_toolchain_schema_valid():
    valid_toolchain = {
        "tools": [
            {"name": "tool1", "description": "Test tool", "parameters": {"param1": "value1"}}
        ],
        "workflow": [
            {"tool": "tool1", "input": {"param1": "value1"}}
        ]
    }
    # Should not raise an exception
    validate_toolchain_schema(valid_toolchain)

def test_validate_toolchain_schema_invalid():
    invalid_toolchain = {
        "tools": [
            {"name": "tool1", "description": "Test tool"}  # Missing 'parameters'
        ],
        "workflow": [
            {"tool": "tool1", "input": {"param1": "value1"}}
        ]
    }
    with pytest.raises(Exception):
        validate_toolchain_schema(invalid_toolchain)

@patch("gpt_dynamic_toolchain.simulate_tool_execution")
def test_execute_toolchain(mock_simulate):
    mock_simulate.return_value = {"simulated_output": "Mocked output"}

    toolchain = {
        "tools": [
            {"name": "tool1", "description": "Test tool", "parameters": {"param1": "value1"}}
        ],
        "workflow": [
            {"tool": "tool1", "input": {"param1": "value1"}}
        ]
    }

    outputs = execute_toolchain(toolchain)
    assert len(outputs) == 1
    assert outputs[0]["tool"] == "tool1"
    assert outputs[0]["output"] == {"simulated_output": "Mocked output"}