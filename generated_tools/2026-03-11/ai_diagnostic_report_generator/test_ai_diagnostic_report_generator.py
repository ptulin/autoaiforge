import pytest
import json
from unittest.mock import patch, mock_open
from ai_diagnostic_report_generator import generate_report

def test_generate_report_json():
    predictions = {"tumor_probability": 0.85}
    metadata = {"patient_id": "12345"}

    with patch("builtins.open", mock_open()) as mocked_file:
        output_file = generate_report(predictions, metadata, output_format='json', output_path='test_report')
        mocked_file.assert_called_once_with("test_report.json", 'w')
        assert output_file == "test_report.json"


def test_generate_report_pdf():
    predictions = {"tumor_probability": 0.85}
    metadata = {"patient_id": "12345"}

    with patch("ai_diagnostic_report_generator.canvas.Canvas") as MockCanvas:
        output_file = generate_report(predictions, metadata, output_format='pdf', output_path='test_report')
        MockCanvas.assert_called_once()
        assert output_file == "test_report.pdf"


def test_generate_report_invalid_format():
    predictions = {"tumor_probability": 0.85}

    with pytest.raises(ValueError, match="Unsupported output format"):
        generate_report(predictions, output_format='xml')