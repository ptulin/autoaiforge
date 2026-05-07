import pytest
import pandas as pd
from adaptive_agent_scheduler import schedule_tasks, load_csv, save_schedule
from unittest.mock import patch, mock_open, MagicMock
import os
import json

def test_load_csv():
    mock_data = "task_id,priority,workload\n1,5,10\n2,3,15"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mocked_file:
        with patch("os.path.exists", return_value=True):
            df = load_csv("dummy.csv")
            assert not df.empty
            assert list(df.columns) == ['task_id', 'priority', 'workload']

def test_schedule_tasks():
    tasks_data = {
        "task_id": [1, 2],
        "priority": [5, 3],
        "workload": [10, 15]
    }
    agents_data = {
        "agent_id": ["A", "B"],
        "availability": [20, 30]
    }

    tasks_df = pd.DataFrame(tasks_data)
    agents_df = pd.DataFrame(agents_data)

    schedule = schedule_tasks(tasks_df, agents_df)

    assert len(schedule) == 2
    assert schedule[0]['agent_id'] in ['A', 'B']
    assert schedule[1]['agent_id'] in ['A', 'B']
    assert schedule[0]['task_id'] == 1
    assert schedule[1]['task_id'] == 2

def test_save_schedule():
    schedule = [
        {"task_id": 1, "agent_id": "A", "priority": 0.5, "workload": 10},
        {"task_id": 2, "agent_id": "B", "priority": 0.3, "workload": 15}
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        save_schedule(schedule, "output.json")
        mocked_file.assert_called_once_with("output.json", "w")
        handle = mocked_file()
        handle.write.assert_called_once_with(json.dumps(schedule, indent=4))

    with patch("pandas.DataFrame.to_csv") as mocked_to_csv:
        save_schedule(schedule, "output.csv")
        mocked_to_csv.assert_called_once()
