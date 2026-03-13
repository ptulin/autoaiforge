import json
import os
import click
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def load_chart_data(input_path):
    """Load JSON chart data from a file."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in input file.")

def generate_plotly_chart(data, output_path):
    """Generate an interactive chart using Plotly and save as HTML."""
    fig = go.Figure()

    for trace in data.get("traces", []):
        if trace["type"] == "scatter":
            fig.add_trace(go.Scatter(x=trace["x"], y=trace["y"], mode=trace.get("mode", "lines"), name=trace.get("name", "")))
        elif trace["type"] == "bar":
            fig.add_trace(go.Bar(x=trace["x"], y=trace["y"], name=trace.get("name", "")))

    fig.update_layout(title=data.get("title", "Chart"), xaxis_title=data.get("xaxis_title", ""), yaxis_title=data.get("yaxis_title", ""))

    fig.write_html(output_path)

def generate_matplotlib_chart(data, output_path):
    """Generate a static chart using Matplotlib and save as an image."""
    plt.figure()

    for trace in data.get("traces", []):
        if trace["type"] == "scatter":
            plt.plot(trace["x"], trace["y"], label=trace.get("name", ""))
        elif trace["type"] == "bar":
            plt.bar(trace["x"], trace["y"], label=trace.get("name", ""))

    plt.title(data.get("title", "Chart"))
    plt.xlabel(data.get("xaxis_title", ""))
    plt.ylabel(data.get("yaxis_title", ""))
    plt.legend()

    plt.savefig(output_path)
    plt.close()

@click.command()
@click.option('--input', 'input_path', required=True, type=click.Path(exists=True), help="Path to the input JSON file.")
@click.option('--output', 'output_path', required=True, type=click.Path(), help="Path to the output file (HTML or image).")
@click.option('--style', 'chart_style', required=True, type=click.Choice(['interactive', 'static']), help="Chart style: 'interactive' for Plotly or 'static' for Matplotlib.")
def main(input_path, output_path, chart_style):
    """AI Chart Converter: Convert AI-generated chart JSON to HTML or image."""
    try:
        chart_data = load_chart_data(input_path)

        if chart_style == 'interactive':
            generate_plotly_chart(chart_data, output_path)
        elif chart_style == 'static':
            generate_matplotlib_chart(chart_data, output_path)

        click.echo(f"Chart successfully saved to {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    main()