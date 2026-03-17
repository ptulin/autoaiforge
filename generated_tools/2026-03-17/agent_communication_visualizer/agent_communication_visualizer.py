import argparse
import networkx as nx
import matplotlib.pyplot as plt
import os

def parse_logs(log_file):
    """
    Parse the log file to extract communication flows.

    Args:
        log_file (str): Path to the log file.

    Returns:
        list of tuples: List of (sender, receiver) communication pairs.
    """
    communication_flows = []
    try:
        with open(log_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    sender, receiver = parts
                    communication_flows.append((sender.strip(), receiver.strip()))
                else:
                    raise ValueError("Invalid log format. Each line must contain exactly one sender and one receiver, separated by a comma.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Log file '{log_file}' not found.")
    except Exception as e:
        raise ValueError(f"Error parsing log file: {e}")

    return communication_flows

def generate_graph(communication_flows, output_file):
    """
    Generate a communication flow graph and save it as a PNG file.

    Args:
        communication_flows (list of tuples): List of (sender, receiver) communication pairs.
        output_file (str): Path to save the output graph PNG file.
    """
    graph = nx.DiGraph()

    for sender, receiver in communication_flows:
        graph.add_edge(sender, receiver)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Agent Communication Flow")
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Agent Communication Visualizer")
    parser.add_argument('--logs', required=True, help="Path to the log file containing agent communication data.")
    parser.add_argument('--output', required=True, help="Path to save the generated communication graph PNG file.")

    args = parser.parse_args()

    try:
        communication_flows = parse_logs(args.logs)
        if not communication_flows:
            print("No communication flows found in the log file.")
            return

        generate_graph(communication_flows, args.output)
        print(f"Communication graph saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()