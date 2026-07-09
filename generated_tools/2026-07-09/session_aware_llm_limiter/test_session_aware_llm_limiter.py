import pytest
from unittest.mock import patch
from session_aware_llm_limiter import Limiter
import time

def test_log_interaction_within_limits():
    limiter = Limiter(query_limit=5, session_duration=10)
    for _ in range(5):
        limiter.log_interaction(user_id='test_user')
    # Should not raise exception

def test_log_interaction_exceeding_query_limit():
    limiter = Limiter(query_limit=3, session_duration=10)
    with pytest.raises(Exception, match="Query limit exceeded"):
        for _ in range(4):
            limiter.log_interaction(user_id='test_user')

def test_log_interaction_exceeding_session_duration():
    limiter = Limiter(query_limit=5, session_duration=1)
    limiter.log_interaction(user_id='test_user')
    time.sleep(2)  # Simulate session duration exceeding
    with pytest.raises(Exception, match="Session duration exceeded"):
        limiter.log_interaction(user_id='test_user')

def test_reset_session():
    limiter = Limiter(query_limit=3, session_duration=10)
    limiter.log_interaction(user_id='test_user')
    limiter.reset_session(user_id='test_user')
    assert 'test_user' not in limiter.sessions

def test_export_sessions():
    limiter = Limiter(query_limit=3, session_duration=10)
    limiter.log_interaction(user_id='test_user')
    exported = limiter.export_sessions()
    assert 'test_user' in exported