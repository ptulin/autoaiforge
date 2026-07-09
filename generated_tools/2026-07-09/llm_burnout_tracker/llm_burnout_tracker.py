import pandas as pd
import matplotlib.pyplot as plt
import click
import os
import json
from datetime import datetime, timedelta

def analyze_logs(data):
    """Analyze user interaction logs to detect signs of burnout."""
    if data.empty:
        return {
            "risk_score": 0,
            "recommendations": ["No data provided to analyze."],
            "analysis": {}
        }

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(by='timestamp', inplace=True)

    # Calculate session lengths
    data['session_diff'] = data['timestamp'].diff().dt.total_seconds()
    session_threshold = 3600  # 1 hour
    data['new_session'] = data['session_diff'] > session_threshold
    data['session_id'] = data['new_session'].cumsum()

    session_stats = data.groupby('session_id').agg(
        session_length=('session_diff', 'sum'),
        query_count=('query', 'count')
    )

    # Calculate risk score
    prolonged_sessions = session_stats[session_stats['session_length'] > 7200]  # Sessions > 2 hours
    high_frequency_sessions = session_stats[session_stats['query_count'] > 50]  # Sessions > 50 queries

    risk_score = min(100, len(prolonged_sessions) * 10 + len(high_frequency_sessions) * 5)

    # Recommendations
    recommendations = []
    if len(prolonged_sessions) > 0:
        recommendations.append("Consider taking breaks during long sessions.")
    if len(high_frequency_sessions) > 0:
        recommendations.append("Reduce the number of queries in a single session.")
    if not recommendations:
        recommendations.append("No signs of burnout detected. Keep up the healthy usage!")

    return {
        "risk_score": risk_score,
        "recommendations": recommendations,
        "analysis": {
            "prolonged_sessions": len(prolonged_sessions),
            "high_frequency_sessions": len(high_frequency_sessions)
        }
    }

def generate_visualization(data, output_path):
    """Generate a visualization of user engagement metrics."""
    if data.empty:
        print("No data available for visualization.")
        return

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['hour'] = data['timestamp'].dt.hour

    hourly_counts = data.groupby('hour').size()

    plt.figure(figsize=(10, 6))
    hourly_counts.plot(kind='bar', color='skyblue')
    plt.title('User Engagement by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Queries')
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

@click.command()
@click.option('--input', 'input_path', required=True, type=click.Path(exists=True), help='Path to the input CSV or JSON file.')
@click.option('--output', 'output_path', required=True, type=click.Path(), help='Path to save the burnout report.')
@click.option('--visual', 'visual_path', required=False, type=click.Path(), help='Path to save the visualization.')
def main(input_path, output_path, visual_path):
    """LLM Burnout Tracker: Analyze user interaction logs to detect signs of burnout."""
    try:
        # Load data
        if input_path.endswith('.csv'):
            data = pd.read_csv(input_path)
        elif input_path.endswith('.json'):
            data = pd.read_json(input_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")

        # Validate required columns
        if 'timestamp' not in data.columns or 'query' not in data.columns:
            raise ValueError("Input file must contain 'timestamp' and 'query' columns.")

        # Analyze logs
        results = analyze_logs(data)

        # Save results to output file
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Burnout report saved to {output_path}")

        # Generate visualization if requested
        if visual_path:
            generate_visualization(data, visual_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
