import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from llm_optimizer_tuner import simulate_workload, generate_report, optimize

def test_simulate_workload():
    config = {
        "classification": {"model": "model_a"},
        "translation": {"model": "model_b"}
    }
    tasks = [
        {"name": "task1", "type": "classification"},
        {"name": "task2", "type": "translation"}
    ]

    metrics = simulate_workload(config, tasks)

    assert len(metrics) == 2
    assert set(metrics.columns) == {"task", "model", "latency", "cost"}
    assert metrics.iloc[0]['model'] == "model_a"
    assert metrics.iloc[1]['model'] == "model_b"

def test_generate_report():
    metrics = pd.DataFrame([
        {"task": "task1", "model": "model_a", "latency": 1.2, "cost": 0.05},
        {"task": "task2", "model": "model_b", "latency": 0.8, "cost": 0.03}
    ])

    with patch("pandas.DataFrame.to_csv") as mocked_to_csv:
        generate_report(metrics, "output.csv")
        mocked_to_csv.assert_called_once_with("output.csv", index=False, encoding="utf-8")

def test_optimize():
    config_content = """
    classification:
      model: model_a
    translation:
      model: model_b
    """

    tasks_content = '[{"name": "task1", "type": "classification"}, {"name": "task2", "type": "translation"}]'

    mock_open_config = mock_open(read_data=config_content)
    mock_open_tasks = mock_open(read_data=tasks_content)

    def side_effect(file, mode):
        if file == "config.yaml":
            return mock_open_config()
        elif file == "tasks.json":
            return mock_open_tasks()
        else:
            raise FileNotFoundError(f"No such file: {file}")

    with patch("builtins.open", side_effect=side_effect) as mocked_open:
        with patch("llm_optimizer_tuner.generate_report") as mocked_generate_report:
            mocked_generate_report.return_value = None  # Mock the generate_report function

            optimize("config.yaml", "tasks.json")

            mocked_open.assert_any_call("config.yaml", "r")
            mocked_open.assert_any_call("tasks.json", "r")
            mocked_generate_report.assert_called_once()
