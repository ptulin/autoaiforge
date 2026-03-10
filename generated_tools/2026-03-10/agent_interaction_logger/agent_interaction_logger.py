from loguru import logger
import json
import pandas as pd
import os

class InteractionLogger:
    def __init__(self, output_path="logs", log_format="json"):
        """
        Initialize the InteractionLogger.

        Args:
            output_path (str): Directory where logs will be saved.
            log_format (str): Format of the logs, either 'json' or 'csv'.
        """
        self.output_path = output_path
        self.log_format = log_format.lower()

        if self.log_format not in ["json", "csv"]:
            raise ValueError("Invalid log format. Choose 'json' or 'csv'.")

        os.makedirs(self.output_path, exist_ok=True)
        self.logs = []

    def log_interaction(self, agent_state, action, environment_feedback):
        """
        Log an interaction between the agent and its environment.

        Args:
            agent_state (dict): Current state of the agent.
            action (dict): Action taken by the agent.
            environment_feedback (dict): Feedback from the environment.
        """
        log_entry = {
            "agent_state": agent_state,
            "action": action,
            "environment_feedback": environment_feedback
        }
        self.logs.append(log_entry)
        logger.info(f"Logged interaction: {log_entry}")

    def save_logs(self, filename="interactions"):
        """
        Save the logged interactions to a file.

        Args:
            filename (str): Base name of the log file (without extension).
        """
        file_path = os.path.join(self.output_path, f"{filename}.{self.log_format}")

        if self.log_format == "json":
            with open(file_path, "w") as f:
                json.dump(self.logs, f, indent=4)
        elif self.log_format == "csv":
            df = pd.DataFrame(self.logs)
            df.to_csv(file_path, index=False)

        logger.info(f"Logs saved to {file_path}")

    def filter_logs(self, filter_func):
        """
        Filter logged interactions based on a custom filter function.

        Args:
            filter_func (callable): A function that takes a log entry and returns True if it should be included.

        Returns:
            list: Filtered log entries.
        """
        return list(filter(filter_func, self.logs))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Agent Interaction Logger")
    parser.add_argument("--output_path", type=str, default="logs", help="Directory to save logs.")
    parser.add_argument("--log_format", type=str, choices=["json", "csv"], default="json", help="Log format.")
    parser.add_argument("--filename", type=str, default="interactions", help="Base name of the log file.")

    args = parser.parse_args()

    logger_instance = InteractionLogger(output_path=args.output_path, log_format=args.log_format)

    # Example usage
    logger_instance.log_interaction(
        agent_state={"position": [0, 0], "health": 100},
        action={"move": "forward"},
        environment_feedback={"reward": 10, "done": False}
    )
    logger_instance.save_logs(filename=args.filename)
