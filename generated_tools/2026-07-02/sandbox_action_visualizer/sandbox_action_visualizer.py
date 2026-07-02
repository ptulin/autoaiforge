import argparse
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sandbox Action Visualizer: Generate visualizations of AI agent behaviors from logs."
    )
    parser.add_argument(
        "--logfile", required=True, help="Path to the AI agent log file (JSON or CSV)."
    )
    parser.add_argument(
        "--output", required=False, help="Path to save the visualization image (optional)."
    )
    parser.add_argument(
        "--filter-agent", required=False, help="Filter logs by a specific agent ID (optional)."
    )
    parser.add_argument(
        "--filter-action", required=False, help="Filter logs by a specific action type (optional)."
    )
    return parser.parse_args()

def load_logs(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Log file '{filepath}' not found.")

    file_extension = os.path.splitext(filepath)[1].lower()
    if file_extension == ".json":
        with open(filepath, "r") as file:
            data = json.load(file)
        return pd.DataFrame(data)
    elif file_extension == ".csv":
        return pd.read_csv(filepath)
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")

def filter_logs(df, agent=None, action=None):
    if agent:
        df = df[df["agent_id"] == agent]
    if action:
        df = df[df["action"] == action]
    return df

def generate_visualization(df, output_path=None):
    if df.empty:
        raise ValueError("No data to visualize after applying filters.")

    if "timestamp" not in df.columns or "action" not in df.columns or "agent_id" not in df.columns:
        raise ValueError("Log file must contain 'timestamp', 'action', and 'agent_id' columns.")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")

    plt.figure(figsize=(10, 6))
    for agent_id, group in df.groupby("agent_id"):
        plt.plot(group["timestamp"], group["action"], marker="o", label=f"Agent {agent_id}")

    plt.xlabel("Timestamp")
    plt.ylabel("Action")
    plt.title("Agent Actions Over Time")
    plt.legend()
    plt.grid(True)

    if output_path:
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    else:
        plt.show()

def main():
    args = parse_arguments()

    try:
        logs_df = load_logs(args.logfile)
        filtered_logs = filter_logs(logs_df, agent=args.filter_agent, action=args.filter_action)
        generate_visualization(filtered_logs, output_path=args.output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()