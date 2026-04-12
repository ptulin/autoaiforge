import pytest
from unittest.mock import patch, mock_open
from ai_zero_day_scanner import analyze_code, generate_report

def test_analyze_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_code("non_existent_file.py")

@patch("builtins.open", new_callable=mock_open, read_data="print('Hello, world!')")
@patch("ai_zero_day_scanner.pipeline")
def test_analyze_code_success(mock_pipeline, mock_file):
    mock_pipeline.return_value = lambda x, truncation: [{"label": "LOW", "score": 0.85}]
    with patch("os.path.isfile", return_value=True):
        results = analyze_code("test_file.py")
        assert len(results) == 1
        assert results[0]['label'] == "LOW"
        assert results[0]['score'] == 0.85

@patch("ai_zero_day_scanner.Table")
@patch("builtins.open", new_callable=mock_open)
def test_generate_report(mock_open, mock_table):
    results = [{"line": 1, "label": "HIGH", "score": 0.95}]
    mock_table.return_value.__str__.return_value = "Mocked Table Output"
    generate_report(results, "output.txt")
    mock_open.assert_called_once_with("output.txt", "w")
    mock_open().write.assert_called_once_with("Mocked Table Output")