import argparse
import json
import threading
import time
from flask import Flask, jsonify, render_template
from rich.console import Console
from rich.table import Table

app = Flask(__name__)

# Shared state for task monitoring
task_data = []
lock = threading.Lock()

@app.route('/')
def dashboard():
    """Render the web dashboard."""
    return render_template('dashboard.html')

@app.route('/api/tasks')
def api_tasks():
    """API endpoint to fetch task data."""
    with lock:
        return jsonify(task_data)

def load_tasks_from_json(file_path):
    """Load tasks from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        Console().print("[red]Error: File not found.")
        return []
    except json.JSONDecodeError:
        Console().print("[red]Error: Invalid JSON format.")
        return []

def monitor_tasks(tasks):
    """Simulate monitoring tasks in real-time."""
    global task_data
    for task in tasks:
        task['status'] = 'in_progress'
    
    while tasks:
        time.sleep(2)  # Simulate task progress
        with lock:
            for task in tasks:
                if task['status'] == 'in_progress':
                    task['progress'] += 10
                    if task['progress'] >= 100:
                        task['status'] = 'completed'
                        Console().print(f"[green]Task {task['id']} completed.")
            task_data = tasks

        tasks = [task for task in tasks if task['status'] != 'completed']

def start_web_dashboard():
    """Start the Flask web dashboard."""
    app.run(debug=False, use_reloader=False)

def main():
    parser = argparse.ArgumentParser(description="Claude Auto Task Monitor")
    parser.add_argument('--input', type=str, required=True, help="Path to the input JSON file containing task details.")
    args = parser.parse_args()

    tasks = load_tasks_from_json(args.input)
    if not tasks:
        Console().print("[red]No tasks to monitor.")
        return

    Console().print("[blue]Starting task monitoring...")

    # Start the web dashboard in a separate thread
    dashboard_thread = threading.Thread(target=start_web_dashboard)
    dashboard_thread.daemon = True
    dashboard_thread.start()

    # Monitor tasks
    monitor_tasks(tasks)

if __name__ == '__main__':
    main()