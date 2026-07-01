import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from kernel_fusion_profiler import profile_script, analyze_fusion_opportunities, visualize_profiling_data

def test_profile_script_file_not_found():
    with pytest.raises(FileNotFoundError):
        profile_script("non_existent_script.py")

@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("kernel_fusion_profiler.profile")
def test_profile_script_mocked(mock_profile, mock_open_file, mock_path_exists):
    mock_event = MagicMock()
    mock_event.key = "kernel1"
    mock_event.cpu_time_total = 100
    mock_event.cuda_time_total = 200
    mock_event.count = 1
    mock_profile.return_value.__enter__.return_value.key_averages.return_value = [mock_event]

    result = profile_script("dummy_script.py")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ["name", "cpu_time", "cuda_time", "occurrences"]
    assert result.iloc[0]["name"] == "kernel1"
    assert result.iloc[0]["cpu_time"] == 100
    assert result.iloc[0]["cuda_time"] == 200
    assert result.iloc[0]["occurrences"] == 1

def test_analyze_fusion_opportunities():
    data = pd.DataFrame({
        "name": ["kernel1", "kernel2"],
        "cpu_time": [100, 200],
        "cuda_time": [1500, 800],
        "occurrences": [2, 1]
    })
    suggestions = analyze_fusion_opportunities(data)
    assert len(suggestions) == 1
    assert "kernel1" in suggestions[0]

@patch("seaborn.barplot")
@patch("matplotlib.pyplot.savefig")
def test_visualize_profiling_data(mock_savefig, mock_barplot):
    data = pd.DataFrame({
        "name": ["kernel1", "kernel2"],
        "cuda_time": [1500, 800]
    })
    visualize_profiling_data(data)
    mock_barplot.assert_called_once()
    mock_savefig.assert_called_once_with("profiling_results.png")