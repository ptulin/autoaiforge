import pandas as pd
import numpy as np

def track_changes(dataset_v1, dataset_v2):
    """
    Compares two datasets containing input-output pairs and expected outputs.

    Args:
        dataset_v1 (pd.DataFrame): First dataset with columns ['input', 'output', 'expected'].
        dataset_v2 (pd.DataFrame): Second dataset with columns ['input', 'output', 'expected'].

    Returns:
        dict: A dictionary containing metrics and change summaries.
    """
    # Validate input
    required_columns = {'input', 'output', 'expected'}
    if not required_columns.issubset(dataset_v1.columns) or not required_columns.issubset(dataset_v2.columns):
        raise ValueError("Both datasets must contain 'input', 'output', and 'expected' columns.")

    # Ensure datasets are aligned by input
    merged = pd.merge(dataset_v1, dataset_v2, on='input', suffixes=('_v1', '_v2'), how='outer')

    # Fill missing values with NaN to handle edge cases
    merged['output_v1'] = merged['output_v1'].fillna(np.nan)
    merged['output_v2'] = merged['output_v2'].fillna(np.nan)
    merged['expected_v1'] = merged['expected_v1'].fillna(np.nan)
    merged['expected_v2'] = merged['expected_v2'].fillna(np.nan)

    # Calculate performance metrics
    merged['correct_v1'] = merged['output_v1'] == merged['expected_v1']
    merged['correct_v2'] = merged['output_v2'] == merged['expected_v2']

    # Calculate deltas
    merged['delta'] = merged['correct_v2'].astype(int) - merged['correct_v1'].astype(int)

    # Summarize changes
    total_samples = len(merged)
    improved = (merged['delta'] > 0).sum()
    worsened = (merged['delta'] < 0).sum()
    unchanged = (merged['delta'] == 0).sum()

    summary = {
        'total_samples': total_samples,
        'improved': improved,
        'worsened': worsened,
        'unchanged': unchanged,
        'improvement_rate': improved / total_samples if total_samples > 0 else 0,
        'worsening_rate': worsened / total_samples if total_samples > 0 else 0
    }

    return {
        'summary': summary,
        'details': merged
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Claude Change Tracker")
    parser.add_argument("dataset_v1", type=str, help="Path to the first dataset (CSV format).")
    parser.add_argument("dataset_v2", type=str, help="Path to the second dataset (CSV format).")
    parser.add_argument("output", type=str, help="Path to save the output summary (CSV format).")

    args = parser.parse_args()

    # Load datasets
    try:
        dataset_v1 = pd.read_csv(args.dataset_v1)
        dataset_v2 = pd.read_csv(args.dataset_v2)
    except Exception as e:
        print(f"Error loading datasets: {e}")
        exit(1)

    # Track changes
    try:
        result = track_changes(dataset_v1, dataset_v2)
        result['details'].to_csv(args.output, index=False)
        print("Change tracking complete. Summary:")
        print(result['summary'])
    except Exception as e:
        print(f"Error during change tracking: {e}")
        exit(1)