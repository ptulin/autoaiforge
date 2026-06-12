import pytest
from unittest.mock import Mock
from token_budget_manager import TokenBudgetManager

def test_track_within_limit():
    mock_api_call = Mock(return_value="This is a test response.")
    manager = TokenBudgetManager(token_limit=1000, token_costs={"mock_api": 50})

    response = manager.track(mock_api_call, api_name="mock_api")

    assert response == "This is a test response."
    assert manager.get_remaining_tokens() < 1000

def test_track_exceed_limit():
    mock_api_call = Mock(return_value="This is a test response.")
    manager = TokenBudgetManager(token_limit=10, token_costs={"mock_api": 5})

    with pytest.raises(RuntimeError, match="Token limit exceeded"):
        manager.track(mock_api_call, api_name="mock_api")

def test_reset():
    mock_api_call = Mock(return_value="This is a test response.")
    manager = TokenBudgetManager(token_limit=1000, token_costs={"mock_api": 50})

    manager.track(mock_api_call, api_name="mock_api")
    manager.reset()

    assert manager.get_remaining_tokens() == 1000
