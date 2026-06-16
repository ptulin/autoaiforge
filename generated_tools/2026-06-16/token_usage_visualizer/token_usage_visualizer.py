import pandas as pd
import matplotlib.pyplot as plt
import click
from io import StringIO

def parse_log_file(file_path):
    """
    Parses a CSV log file containing token usage data.

    Args:
        file_path (str): Path to the log file.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed token usage data.
    """
    try:
        data = pd.read_csv(file_path, parse_dates=['timestamp'])
        if 'timestamp' not in data.columns or 'tokens' not in data.columns:
            raise ValueError("CSV file must contain 'timestamp' and 'tokens' columns.")
        return data
    except Exception as e:
        raise ValueError(f"Error reading log file: {e}")

def generate_line_chart(data, output_file=None):
    """
    Generates a line chart of token usage over time.

    Args:
        data (pd.DataFrame): Token usage data.
        output_file (str, optional): Path to save the chart image. Defaults to None.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data['timestamp'], data['tokens'], label='Token Usage', color='blue')
    plt.xlabel('Timestamp')
    plt.ylabel('Tokens')
    plt.title('Token Usage Over Time')
    plt.legend()
    plt.grid()

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def generate_bar_chart(data, output_file=None):
    """
    Generates a bar chart of token usage over time.

    Args:
        data (pd.DataFrame): Token usage data.
        output_file (str, optional): Path to save the chart image. Defaults to None.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    plt.bar(data['timestamp'], data['tokens'], label='Token Usage', color='green')
    plt.xlabel('Timestamp')
    plt.ylabel('Tokens')
    plt.title('Token Usage Over Time')
    plt.legend()
    plt.grid()

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def generate_pie_chart(data, output_file=None):
    """
    Generates a pie chart of token usage distribution.

    Args:
        data (pd.DataFrame): Token usage data.
        output_file (str, optional): Path to save the chart image. Defaults to None.

    Returns:
        None
    """
    usage_by_day = data.groupby(data['timestamp'].dt.date)['tokens'].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(usage_by_day, labels=usage_by_day.index, autopct='%1.1f%%', startangle=140)
    plt.title('Token Usage Distribution by Day')

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

@click.command()
@click.option('--log_file', type=click.Path(exists=True), required=True, help='Path to the token usage log file (CSV).')
@click.option('--chart_type', type=click.Choice(['line', 'bar', 'pie'], case_sensitive=False), required=True, help='Type of chart to generate.')
@click.option('--output', type=click.Path(), default=None, help='Path to save the chart image (optional).')
def main(log_file, chart_type, output):
    """
    CLI entry point for the Token Usage Visualizer tool.
    """
    try:
        data = parse_log_file(log_file)

        if chart_type == 'line':
            generate_line_chart(data, output)
        elif chart_type == 'bar':
            generate_bar_chart(data, output)
        elif chart_type == 'pie':
            generate_pie_chart(data, output)

        if output:
            click.echo(f"Chart saved to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    main()
