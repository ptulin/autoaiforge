import pytest
import pandas as pd
from unittest.mock import Mock
from ethical_ai_tester import EthicalAITester

def test_bias_detection():
    config = {
        'bias': {
            'group_column': 'group',
            'input_column': 'input',
            'threshold': 0.1
        }
    }
    test_data = pd.DataFrame({
        'group': ['A', 'A', 'B', 'B'],
        'input': [1, 2, 3, 4]
    })
    model = Mock(side_effect=lambda x: [0.1, 0.2, 0.9, 1.0])

    tester = EthicalAITester(config)
    tester.test_bias(lambda inputs: [0.1 if i in [1, 2] else 0.9 for i in inputs], test_data)

    assert tester.results[0]['test'] == 'bias'
    assert tester.results[0]['result'] == 'failed'
    assert 'Bias detected' in tester.results[0]['reason']

def test_fairness_detection():
    config = {
        'fairness': {
            'input_column': 'input',
            'min_unique_predictions': 2
        }
    }
    test_data = pd.DataFrame({
        'input': [1, 2, 3, 4]
    })
    model = Mock(side_effect=lambda x: [0, 0, 1, 1])

    tester = EthicalAITester(config)
    tester.test_fairness(model, test_data)

    assert tester.results[0]['test'] == 'fairness'
    assert tester.results[0]['result'] == 'passed'

def test_empty_data():
    config = {
        'bias': {
            'group_column': 'group',
            'input_column': 'input',
            'threshold': 0.1
        }
    }
    test_data = pd.DataFrame()
    model = Mock(return_value=[])

    tester = EthicalAITester(config)
    tester.test_bias(model, test_data)

    assert tester.results[0]['test'] == 'bias'
    assert tester.results[0]['result'] == 'failed'
    assert 'Empty test data' in tester.results[0]['reason']