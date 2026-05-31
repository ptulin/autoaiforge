import pytest
from unittest.mock import MagicMock, patch
from llm_usage_tracker import Tracker, UsageLog
import pandas as pd

def test_log_usage():
    tracker = Tracker(db_url='sqlite:///:memory:')
    tracker.log_usage(api_key='test_key', tokens_used=100, user_id='test_user')

    session = tracker.Session()
    logs = session.query(UsageLog).all()
    session.close()

    assert len(logs) == 1
    assert logs[0].api_key == 'test_key'
    assert logs[0].tokens_used == 100
    assert logs[0].user_id == 'test_user'

def test_log_usage_invalid_input():
    tracker = Tracker(db_url='sqlite:///:memory:')
    with pytest.raises(ValueError):
        tracker.log_usage(api_key='', tokens_used=-1, user_id='')

def test_generate_report():
    tracker = Tracker(db_url='sqlite:///:memory:')
    tracker.log_usage(api_key='test_key', tokens_used=100, user_id='test_user')

    with patch('rich.console.Console.print') as mock_print:
        tracker.generate_report(output_format='table')
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        assert 'test_key' in str(args)
        assert 'test_user' in str(args)
        assert '100' in str(args)