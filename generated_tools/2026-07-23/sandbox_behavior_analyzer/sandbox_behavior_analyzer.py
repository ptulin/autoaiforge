import json
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import argparse

def parse_logs(file_path):
    """Parses log files in JSON or CSV format into a Pandas DataFrame."""
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Use JSON or CSV.")
    except Exception as e:
        raise ValueError(f"Error reading log file: {e}")

def preprocess_logs(df):
    """Preprocesses the logs for analysis by handling missing values and scaling."""
    df = df.fillna(0)  # Replace missing values with 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df, numeric_cols

def detect_anomalies(df, numeric_cols):
    """Detects anomalies in the logs using Isolation Forest."""
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[numeric_cols])
    df['risk_score'] = zscore(df['anomaly_score'])
    anomalies = df[df['anomaly_score'] == -1]
    return anomalies[['risk_score']]

def analyze_logs(file_path):
    """Main function to analyze logs and return flagged anomalies with risk scores."""
    try:
        logs = parse_logs(file_path)
        processed_logs, numeric_cols = preprocess_logs(logs)
        anomalies = detect_anomalies(processed_logs, numeric_cols)
        return anomalies
    except Exception as e:
        raise RuntimeError(f"Failed to analyze logs: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sandbox Behavior Analyzer")
    parser.add_argument('file_path', type=str, help="Path to the log file (JSON or CSV)")
    args = parser.parse_args()

    try:
        anomalies = analyze_logs(args.file_path)
        print("Anomalies detected:")
        print(anomalies)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()