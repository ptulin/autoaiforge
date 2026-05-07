import argparse
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
import os

def load_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def schedule_tasks(tasks_df, agents_df):
    if tasks_df.empty or agents_df.empty:
        raise ValueError("Tasks or agents data is empty.")

    # Ensure required columns exist
    required_task_columns = {'task_id', 'priority', 'workload'}
    required_agent_columns = {'agent_id', 'availability'}

    if not required_task_columns.issubset(tasks_df.columns):
        raise ValueError(f"Tasks CSV must contain columns: {required_task_columns}")
    if not required_agent_columns.issubset(agents_df.columns):
        raise ValueError(f"Agents CSV must contain columns: {required_agent_columns}")

    # Normalize priority and availability
    tasks_df['priority'] = tasks_df['priority'] / tasks_df['priority'].max()
    agents_df['availability'] = agents_df['availability'] / agents_df['availability'].max()

    # Assign tasks to agents based on availability and priority
    schedule = []
    for _, task in tasks_df.iterrows():
        best_agent = agents_df.loc[agents_df['availability'].idxmax()]
        schedule.append({
            "task_id": task['task_id'],
            "agent_id": best_agent['agent_id'],
            "priority": task['priority'],
            "workload": task['workload']
        })
        # Reduce agent availability after assigning a task
        agents_df.loc[agents_df['agent_id'] == best_agent['agent_id'], 'availability'] -= task['workload']

    return schedule

def save_schedule(schedule, output_path):
    if output_path.endswith('.csv'):
        pd.DataFrame(schedule).to_csv(output_path, index=False)
    elif output_path.endswith('.json'):
        with open(output_path, 'w') as f:
            f.write(json.dumps(schedule, indent=4))
    else:
        raise ValueError("Output file must be .csv or .json")

def main():
    parser = argparse.ArgumentParser(description="Adaptive Agent Scheduler")
    parser.add_argument('--tasks', required=True, help="Path to tasks CSV file")
    parser.add_argument('--agents', required=True, help="Path to agents CSV file")
    parser.add_argument('--output', required=True, help="Path to output file (CSV or JSON)")

    args = parser.parse_args()

    try:
        tasks_df = load_csv(args.tasks)
        agents_df = load_csv(args.agents)

        schedule = schedule_tasks(tasks_df, agents_df)

        save_schedule(schedule, args.output)
        print(f"Schedule saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
