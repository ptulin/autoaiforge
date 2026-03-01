import pytest
import pandas as pd
import yaml
from unittest.mock import patch, mock_open
from decision_audit_tool import load_rules, load_log, audit_decisions

def test_load_rules():
    mock_yaml = """
    rules:
      - condition: "row['action'] == 'attack' and row['target'] == 'civilian'"
        explanation: "Attacking civilians is prohibited."
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        rules = load_rules("rules.yaml")
        assert 'rules' in rules
        assert len(rules['rules']) == 1
        assert rules['rules'][0]['condition'] == "row['action'] == 'attack' and row['target'] == 'civilian'"

def test_load_log_csv():
    mock_csv = "decision_id,action,target\n1,attack,civilian\n2,defend,base"
    with patch("os.path.exists", return_value=True):
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({
                'decision_id': [1, 2],
                'action': ['attack', 'defend'],
                'target': ['civilian', 'base']
            })
            log_df = load_log("log.csv")
            assert len(log_df) == 2
            assert log_df.loc[0, 'action'] == 'attack'

def test_audit_decisions():
    log_df = pd.DataFrame({
        'decision_id': [1, 2],
        'action': ['attack', 'defend'],
        'target': ['civilian', 'base']
    })
    rules = {
        'rules': [
            {
                'condition': "row['action'] == 'attack' and row['target'] == 'civilian'",
                'explanation': "Attacking civilians is prohibited."
            }
        ]
    }
    flagged_decisions = audit_decisions(log_df, rules)
    assert len(flagged_decisions) == 1
    assert flagged_decisions[0]['decision_id'] == 1
    assert flagged_decisions[0]['explanation'] == "Attacking civilians is prohibited."