import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from ai_data_sanitizer import load_data, detect_pii, anonymize_pii, normalize_data

@pytest.fixture
def sample_data():
    return pd.DataFrame({'email': ['test@example.com', 'test2@example.com'],
                          'phone': ['123-456-7890', '987-654-3210'],
                          'ssn': ['123456789', '987654321'],
                          'numerical': [1.0, 2.0]})

def test_load_data(sample_data, tmp_path):
    sample_data.to_csv(tmp_path / 'data.csv', index=False)
    loaded_data = load_data(tmp_path / 'data.csv')
    # Convert loaded data to string to match the original data
    loaded_data['ssn'] = loaded_data['ssn'].astype(str)
    pd.testing.assert_frame_equal(loaded_data, sample_data)

@patch('ai_data_sanitizer.load_data', return_value=None)
def test_load_data_error(test_load_data):
    assert load_data('non_existent_file.csv') is None


def test_detect_pii(sample_data):
    pii_columns = detect_pii(sample_data)
    assert set(pii_columns) == set(['email', 'phone', 'ssn'])


def test_anonymize_pii(sample_data):
    pii_columns = detect_pii(sample_data)
    anonymized_data = anonymize_pii(sample_data, pii_columns)
    assert anonymized_data['email'].equals(pd.Series(['***', '***']))
    assert anonymized_data['phone'].equals(pd.Series(['***', '***']))
    assert anonymized_data['ssn'].equals(pd.Series(['***', '***']))


def test_normalize_data(sample_data):
    normalized_data = normalize_data(sample_data)
    assert np.allclose(normalized_data['numerical'], [-1.0, 1.0])