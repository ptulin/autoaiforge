import json
import plotly.graph_objects as go
import pandas as pd
from IPython.display import display

def render_chart(chart_data):
    """
    Render an interactive chart in a Jupyter notebook based on AI-generated chart data.

    Args:
        chart_data (dict or str): A dictionary or JSON string containing chart data.

    Raises:
        ValueError: If the input data is invalid or cannot be parsed.
    """
    if isinstance(chart_data, str):
        try:
            chart_data = json.loads(chart_data)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON string provided.") from e

    if not isinstance(chart_data, dict):
        raise ValueError("Input data must be a dictionary or a valid JSON string.")

    # Validate required keys
    required_keys = {"type", "data", "layout"}
    if not required_keys.issubset(chart_data.keys()):
        raise ValueError(f"Input data must contain the keys: {required_keys}")

    # Extract chart type, data, and layout
    chart_type = chart_data["type"].lower()
    data = chart_data["data"]
    layout = chart_data.get("layout", {})

    if not isinstance(data, list) or not all(isinstance(trace, dict) for trace in data):
        raise ValueError("'data' must be a list of dictionaries.")

    if chart_type == "scatter":
        fig = go.Figure()
        for trace in data:
            fig.add_trace(go.Scatter(**trace))
    elif chart_type == "bar":
        fig = go.Figure()
        for trace in data:
            fig.add_trace(go.Bar(**trace))
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    fig.update_layout(**layout)
    display(fig)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Interactive Chart Injector")
    parser.add_argument("chart_data", type=str, help="Path to a JSON file containing chart data.")

    args = parser.parse_args()

    try:
        with open(args.chart_data, "r") as f:
            chart_data = json.load(f)
        render_chart(chart_data)
    except Exception as e:
        print(f"Error: {e}")