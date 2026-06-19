import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock
from rare_disease_diagnostic_assistant import load_model, load_patient_data, generate_diagnostic_report, save_report

def test_load_model():
    with patch('joblib.load') as mock_load:
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        model = load_model('mock_model.pkl')
        assert model == mock_model
        mock_load.assert_called_once_with('mock_model.pkl')

def test_load_patient_data_csv():
    with patch('pandas.read_csv') as mock_read_csv:
        mock_df = pd.DataFrame({'symptom1': [1], 'symptom2': [0]})
        mock_read_csv.return_value = mock_df
        df = load_patient_data('mock_data.csv')
        assert df.equals(mock_df)
        mock_read_csv.assert_called_once_with('mock_data.csv')

def test_load_patient_data_json():
    with patch('pandas.read_json') as mock_read_json:
        mock_df = pd.DataFrame({'symptom1': [1], 'symptom2': [0]})
        mock_read_json.return_value = mock_df
        df = load_patient_data('mock_data.json')
        assert df.equals(mock_df)
        mock_read_json.assert_called_once_with('mock_data.json')

def test_generate_diagnostic_report():
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = [[0.7, 0.3]]
    mock_model.classes_ = ['DiseaseA', 'DiseaseB']
    patient_data = pd.DataFrame({'symptom1': [1], 'symptom2': [0]})
    report = generate_diagnostic_report(mock_model, patient_data)
    assert len(report) == 1
    assert report[0]['patient_id'] == 0
    assert report[0]['diagnoses'][0]['disease'] == 'DiseaseA'
    assert report[0]['diagnoses'][0]['confidence'] == 0.7

def test_save_report(tmp_path):
    report = [{"patient_id": 0, "diagnoses": [{"disease": "DiseaseA", "confidence": 0.7}]}]
    output_path = tmp_path / "report.json"
    save_report(report, output_path)
    with open(output_path, 'r') as f:
        saved_report = json.load(f)
    assert saved_report == report