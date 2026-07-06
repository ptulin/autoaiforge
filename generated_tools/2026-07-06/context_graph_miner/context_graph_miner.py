import argparse
import json
import networkx as nx
import pandas as pd

def load_context_graph(file_path):
    """Load a context graph from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        graph = nx.node_link_graph(data)
        return graph
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to load graph: {e}")

def query_graph(graph, query):
    """Query the graph for nodes containing the specified substring in their attributes."""
    results = []
    for node, data in graph.nodes(data=True):
        if query in str(data):
            results.append({"node": node, "attributes": data})
    return results

def generate_report(graph, output_format):
    """Generate a report summarizing the graph's nodes and edges."""
    nodes_data = [
        {"node": node, **data} for node, data in graph.nodes(data=True)
    ]
    edges_data = [
        {"source": u, "target": v, **data} for u, v, data in graph.edges(data=True)
    ]

    nodes_df = pd.DataFrame(nodes_data)
    edges_df = pd.DataFrame(edges_data)

    if output_format == "csv":
        nodes_df.to_csv("nodes_report.csv", index=False)
        edges_df.to_csv("edges_report.csv", index=False)
        return "Reports saved as nodes_report.csv and edges_report.csv"
    elif output_format == "json":
        nodes_df.to_json("nodes_report.json", orient="records")
        edges_df.to_json("edges_report.json", orient="records")
        return "Reports saved as nodes_report.json and edges_report.json"
    else:
        raise ValueError("Invalid output format. Use 'csv' or 'json'.")

def main():
    parser = argparse.ArgumentParser(description="Context Graph Miner")
    parser.add_argument("--file", required=True, help="Path to the JSON file containing the context graph")
    parser.add_argument("--query", help="Query string to search for specific nodes")
    parser.add_argument("--report", choices=["csv", "json"], help="Generate a report in the specified format")

    args = parser.parse_args()

    try:
        graph = load_context_graph(args.file)

        if args.query:
            results = query_graph(graph, args.query)
            if results:
                print("Query Results:")
                for result in results:
                    print(result)
            else:
                print("No matching nodes found.")

        if args.report:
            report_message = generate_report(graph, args.report)
            print(report_message)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
