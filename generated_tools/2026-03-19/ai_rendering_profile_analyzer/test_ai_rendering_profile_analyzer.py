import pytest
import pandas as pd
import json
from unittest.mock import patch, mock_open
from ai_rendering_profile_analyzer import analyze_rendering_logs

def test_analyze_rendering_logs_csv(tmp_path):
    # Mock input CSV data
    csv_content = """frame,render_time,gpu_usage,resolution
1,16.7,75,1080
2,18.5,80,1440
3,20.1,85,2160
"""
    input_file = tmp_path / "test.csv"
    output_file = tmp_path / "output.json"
    input_file.write_text(csv_content)

    analyze_rendering_logs(str(input_file), str(output_file), 'json')

    # Validate output
    with open(output_file) as f:
        output_data = json.load(f)

    assert output_data['average_render_time'] == pytest.approx(18.433, 0.001)
    assert output_data['max_gpu_usage'] == 85
    assert output_data['high_resolution_frame_count'] == 2

def test_analyze_rendering_logs_json(tmp_path):
    # Mock input JSON data
    json_content = [
        {"frame": 1, "render_time": 16.7, "gpu_usage": 75, "resolution": 1080},
        {"frame": 2, "render_time": 18.5, "gpu_usage": 80, "resolution": 1440},
        {"frame": 3, "render_time": 20.1, "gpu_usage": 85, "resolution": 2160}
    ]
    input_file = tmp_path / "test.json"
    output_file = tmp_path / "output.txt"
    input_file.write_text(json.dumps(json_content))

    analyze_rendering_logs(str(input_file), str(output_file), 'text')

    # Validate output
    with open(output_file) as f:
        output_text = f.read()

    assert "average_render_time: 18.433333333333334" in output_text
    assert "max_gpu_usage: 85" in output_text
    assert "high_resolution_frame_count: 2" in output_text

def test_analyze_rendering_logs_plot(tmp_path):
    # Mock input CSV data
    csv_content = """frame,render_time,gpu_usage,resolution
1,16.7,75,1080
2,18.5,80,1440
3,20.1,85,2160
"""
    input_file = tmp_path / "test.csv"
    output_file = tmp_path / "output_plot.png"
    input_file.write_text(csv_content)

    analyze_rendering_logs(str(input_file), str(output_file), 'plot')

    # Validate plot file creation
    assert output_file.exists()
    assert output_file.stat().st_size > 0