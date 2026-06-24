import argparse
import json
import sys
from graphviz import Digraph

def parse_arguments():
    parser = argparse.ArgumentParser(description="Agent Decision Tracer: Trace AI agent decisions and visualize execution paths.")
    parser.add_argument('--input', type=str, help="Path to the JSON file containing decision logs. Use '-' for stdin.", required=True)
    parser.add_argument('--output', type=str, help="Path to save the output graph (.dot or .png).", required=True)
    parser.add_argument('--log', type=str, help="Path to save the structured trace logs as JSON.", required=False)
    return parser.parse_args()

def load_decision_logs(input_path):
    if input_path == "-":
        try:
            return json.load(sys.stdin)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON input from stdin.") from e
    else:
        try:
            with open(input_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{input_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file '{input_path}'.") from e

def validate_decision_logs(logs):
    if not isinstance(logs, list):
        raise ValueError("Decision logs must be a list of events.")
    for event in logs:
        if not isinstance(event, dict) or 'step' not in event or 'decision' not in event or 'reasoning' not in event:
            raise ValueError("Each event must be a dictionary with 'step', 'decision', and 'reasoning' keys.")

def generate_execution_graph(logs, output_path):
    graph = Digraph(format=output_path.split('.')[-1])
    for event in logs:
        step = event['step']
        decision = event['decision']
        reasoning = event['reasoning']
        graph.node(str(step), f"Step {step}\nDecision: {decision}\nReasoning: {reasoning}")
        if 'previous_step' in event:
            graph.edge(str(event['previous_step']), str(step))
    graph.render(output_path.rsplit('.', 1)[0], cleanup=True)

def save_trace_logs(logs, log_path):
    if log_path:
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=4)

def main():
    args = parse_arguments()

    try:
        decision_logs = load_decision_logs(args.input)
        validate_decision_logs(decision_logs)
        generate_execution_graph(decision_logs, args.output)
        if args.log:
            save_trace_logs(decision_logs, args.log)
        print(f"Execution graph saved to {args.output}")
        if args.log:
            print(f"Trace logs saved to {args.log}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()