import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import argparse


def load_data(input_path):
    try:
        return pd.read_csv(input_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def detect_pii(data):
    # Simple PII detection: email, phone number, SSN
    pii_columns = []
    for column in data.columns:
        if data[column].astype(str).str.contains('@').any() or \
           data[column].astype(str).str.contains('\d{3}-\d{3}-\d{4}').any() or \
           data[column].astype(str).str.contains('\d{9}').any():
            pii_columns.append(column)
    return pii_columns


def anonymize_pii(data, pii_columns):
    for column in pii_columns:
        data[column] = data[column].apply(lambda x: '***' if isinstance(x, str) else np.nan)
    return data


def normalize_data(data):
    scaler = StandardScaler()
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
    return data


def sanitize_data(input_path, output_path):
    data = load_data(input_path)
    if data is None:
        return
    pii_columns = detect_pii(data)
    data = anonymize_pii(data, pii_columns)
    data = normalize_data(data)
    data.to_csv(output_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Data Sanitizer')
    parser.add_argument('--input-path', required=True, help='Path to the training data file')
    parser.add_argument('--output-path', required=True, help='Path to the sanitized data file')
    args = parser.parse_args()
    sanitize_data(args.input_path, args.output_path)