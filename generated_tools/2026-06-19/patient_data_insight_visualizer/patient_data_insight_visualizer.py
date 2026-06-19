import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

def load_data(file_path):
    """Load data from a CSV or JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")

def generate_visualizations(data, output_file):
    """Generate visualizations and save them to an output file."""
    if data.empty:
        raise ValueError("Input data is empty. Please provide valid data.")

    # Generate a time-series plot if a 'date' column exists
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        if data['date'].isnull().all():
            raise ValueError("The 'date' column contains invalid date values.")

        time_series_fig = px.line(data, x='date', y=data.columns[1:], title='Time-Series Data')
        time_series_fig.write_html(output_file.replace('.html', '_time_series.html'))

    # Generate a heatmap if there are numerical columns
    numerical_columns = data.select_dtypes(include=['number']).columns
    if len(numerical_columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(data[numerical_columns].corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap of Numerical Data')
        heatmap_file = output_file.replace('.html', '_heatmap.png')
        plt.savefig(heatmap_file)
        plt.close()

    # Generate a scatter plot if there are at least two numerical columns
    if len(numerical_columns) >= 2:
        scatter_fig = px.scatter(data, x=numerical_columns[0], y=numerical_columns[1], title='Scatter Plot')
        scatter_fig.write_html(output_file.replace('.html', '_scatter.html'))

def main():
    parser = argparse.ArgumentParser(description="Patient Data Insight Visualizer")
    parser.add_argument('--input', required=True, help="Path to the input CSV or JSON file containing patient data.")
    parser.add_argument('--output', required=True, help="Path to save the output visualizations (HTML or image files).")

    args = parser.parse_args()

    try:
        data = load_data(args.input)
        generate_visualizations(data, args.output)
        print(f"Visualizations successfully saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()