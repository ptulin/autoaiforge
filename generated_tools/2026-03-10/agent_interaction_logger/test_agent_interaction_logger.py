import pytest
from unittest.mock import patch, mock_open
from agent_interaction_logger import InteractionLogger
import os
import json
import pandas as pd

def test_log_interaction():
    logger = InteractionLogger(output_path="test_logs", log_format="json")
    logger.log_interaction(
        agent_state={"position": [0, 0]},
        action={"move": "forward"},
        environment_feedback={"reward": 10}
    )
    assert len(logger.logs) == 1
    assert logger.logs[0]["agent_state"] == {"position": [0, 0]}

def test_save_logs_json():
    logger = InteractionLogger(output_path="test_logs", log_format="json")
    logger.log_interaction(
        agent_state={"position": [0, 0]},
        action={"move": "forward"},
        environment_feedback={"reward": 10}
    )

    with patch("builtins.open", mock_open()) as mocked_file:
        logger.save_logs(filename="test_interactions")
        mocked_file.assert_called_once_with(os.path.join("test_logs", "test_interactions.json"), "w")

        handle = mocked_file()
        handle.write.assert_called()

def test_save_logs_csv():
    logger = InteractionLogger(output_path="test_logs", log_format="csv")
    logger.log_interaction(
        agent_state={"position": [0, 0]},
        action={"move": "forward"},
        environment_feedback={"reward": 10}
    )

    with patch("pandas.DataFrame.to_csv") as mocked_to_csv:
        logger.save_logs(filename="test_interactions")
        mocked_to_csv.assert_called_once_with(os.path.join("test_logs", "test_interactions.csv"), index=False)

def test_filter_logs():
    logger = InteractionLogger(output_path="test_logs", log_format="json")
    logger.log_interaction(
        agent_state={"position": [0, 0]},
        action={"move": "forward"},
        environment_feedback={"reward": 10}
    )
    logger.log_interaction(
        agent_state={"position": [1, 1]},
        action={"move": "backward"},
        environment_feedback={"reward": -5}
    )

    filtered_logs = logger.filter_logs(lambda log: log["environment_feedback"]["reward"] > 0)
    assert len(filtered_logs) == 1
    assert filtered_logs[0]["agent_state"] == {"position": [0, 0]}
