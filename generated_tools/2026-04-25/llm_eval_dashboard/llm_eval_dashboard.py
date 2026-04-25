import argparse
import pandas as pd
import streamlit as st
import json
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load evaluation data from a JSON or CSV file."""
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a .json or .csv file.")
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")

def generate_dashboard(data):
    """Generate an interactive dashboard using Streamlit."""
    st.title("LLM Evaluation Dashboard")

    # Sidebar filters
    st.sidebar.header("Filters")
    models = st.sidebar.multiselect("Select Models", options=list(data['model'].unique()), default=list(data['model'].unique()))
    datasets = st.sidebar.multiselect("Select Datasets", options=list(data['dataset'].unique()), default=list(data['dataset'].unique()))
    tasks = st.sidebar.multiselect("Select Tasks", options=list(data['task'].unique()), default=list(data['task'].unique()))

    # Filter data
    filtered_data = data[(data['model'].isin(models)) &
                         (data['dataset'].isin(datasets)) &
                         (data['task'].isin(tasks))]

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
        return

    # Display data table
    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    # Visualization: Bar chart for metrics
    st.subheader("Metric Comparison")
    metric = st.selectbox("Select Metric", options=[col for col in data.columns if col not in ['model', 'dataset', 'task']])

    if metric:
        metric_data = filtered_data.groupby(['model'])[metric].mean().reset_index()
        fig, ax = plt.subplots()
        ax.bar(metric_data['model'], metric_data[metric], color='skyblue')
        ax.set_title(f"Average {metric} by Model")
        ax.set_ylabel(metric)
        ax.set_xlabel("Model")
        st.pyplot(fig)

    # Visualization: Line chart for latency (if available)
    if 'latency' in data.columns:
        st.subheader("Latency Over Datasets")
        latency_data = filtered_data.groupby(['dataset', 'model'])['latency'].mean().unstack()
        if not latency_data.empty:
            st.line_chart(latency_data)

    st.success("Dashboard generated successfully!")

def main():
    parser = argparse.ArgumentParser(description="LLM Evaluation Dashboard")
    parser.add_argument('--data', type=str, required=True, help="Path to the evaluation results file (JSON or CSV).")
    args = parser.parse_args()

    try:
        data = load_data(args.data)
        st.set_page_config(page_title="LLM Evaluation Dashboard", layout="wide")
        generate_dashboard(data)
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
