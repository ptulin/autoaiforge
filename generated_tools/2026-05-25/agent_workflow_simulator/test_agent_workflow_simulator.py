import pytest
from unittest.mock import patch, MagicMock
import agent_workflow_simulator

def test_simulate_workflow_empty():
    """Test simulation with an empty workflow."""
    with patch('logging.Logger.info') as mock_info, patch('logging.Logger.error') as mock_error:
        agent_workflow_simulator.simulate_workflow({})
        mock_info.assert_any_call("Starting workflow simulation...")
        mock_error.assert_any_call("No steps found in the workflow.")

def test_simulate_workflow_with_steps():
    """Test simulation with valid steps."""
    workflow = {
        "steps": [
            {"name": "Step 1", "action": "Action 1", "execution_time": 0.1},
            {"name": "Step 2", "action": "Action 2", "execution_time": 0.2}
        ]
    }
    with patch('logging.Logger.info') as mock_info:
        agent_workflow_simulator.simulate_workflow(workflow)
        mock_info.assert_any_call("Executing step: Step 1")
        mock_info.assert_any_call("Step 'Step 1' completed in 0.1 seconds.")
        mock_info.assert_any_call("Executing step: Step 2")
        mock_info.assert_any_call("Step 'Step 2' completed in 0.2 seconds.")

def test_simulate_workflow_error_handling():
    """Test simulation with a step causing an error."""
    workflow = {
        "steps": [
            {"name": "Faulty Step", "action": "Faulty Action", "execution_time": "invalid"}
        ]
    }
    with patch('logging.Logger.error') as mock_error:
        agent_workflow_simulator.simulate_workflow(workflow)
        mock_error.assert_any_call("Error during step 'Faulty Step': could not convert string to float: 'invalid'")
