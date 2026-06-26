import pytest
import pandas as pd
import json
from unittest.mock import patch, mock_open
from io import StringIO
from toxic_content_tester import load_csv, load_json, evaluate_outputs, generate_report

def test_load_csv():
    data = "id,content\n1,This is a test\n2,Another test"
    with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(data))):
        df = load_csv("test.csv")
        assert len(df) == 2
        assert list(df.columns) == ['id', 'content']

def test_load_json():
    data = '[{"keyword": "test", "description": "Contains test keyword"}]'
    with patch("builtins.open", mock_open(read_data=data)):
        rules = load_json("rules.json")
        assert len(rules) == 1
        assert rules[0]['keyword'] == "test"

def test_evaluate_outputs():
    outputs = pd.DataFrame([
        {'id': 1, 'content': 'This is a test'},
        {'id': 2, 'content': 'Nothing harmful here'}
    ])
    rules = [{'keyword': 'test', 'description': 'Contains test keyword'}]
    results = evaluate_outputs(outputs, rules)
    assert len(results) == 2
    assert results[0]['flagged_rules'] == ['Contains test keyword']
    assert results[1]['flagged_rules'] == []

def test_generate_report_json(tmp_path):
    results = [
        {'id': 1, 'content': 'This is a test', 'flagged_rules': ['Contains test keyword']},
        {'id': 2, 'content': 'Nothing harmful here', 'flagged_rules': []}
    ]
    report_path = tmp_path / "report.json"
    generate_report(results, report_path, "json")
    with open(report_path, 'r') as f:
        report = json.load(f)
    assert len(report) == 2
    assert report[0]['flagged_rules'] == ['Contains test keyword']

def test_generate_report_html(tmp_path):
    results = [
        {'id': 1, 'content': 'This is a test', 'flagged_rules': ['Contains test keyword']},
        {'id': 2, 'content': 'Nothing harmful here', 'flagged_rules': []}
    ]
    report_path = tmp_path / "report.html"
    generate_report(results, report_path, "html")
    with open(report_path, 'r') as f:
        html_content = f.read()
    assert "<html>" in html_content
    assert "<table" in html_content
    assert "Contains test keyword" in html_content