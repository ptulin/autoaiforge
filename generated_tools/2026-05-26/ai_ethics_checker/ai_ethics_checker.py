import argparse
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from tabulate import tabulate

def load_model(model_path):
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")

def load_dataset(dataset_path):
    try:
        return pd.read_csv(dataset_path)
    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")

def load_guidelines(guidelines_path):
    try:
        with open(guidelines_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Error loading guidelines: {e}")

def check_bias(dataset):
    if dataset.empty:
        return "Dataset is empty. Cannot check for bias."
    bias_report = {}
    for column in dataset.select_dtypes(include=['object', 'category']):
        counts = dataset[column].value_counts(normalize=True)
        bias_report[column] = counts.to_dict()
    return bias_report

def evaluate_model(model, dataset):
    if dataset.empty:
        return "Dataset is empty. Cannot evaluate model."
    if 'target' not in dataset.columns:
        return "Dataset must contain a 'target' column for evaluation."

    X = dataset.drop(columns=['target'])
    y = dataset['target']

    try:
        predictions = model.predict(X)
        accuracy = accuracy_score(y, predictions)
        conf_matrix = confusion_matrix(y, predictions).tolist()
        return {
            "accuracy": accuracy,
            "confusion_matrix": conf_matrix
        }
    except Exception as e:
        return f"Error evaluating model: {e}"

def generate_report(bias_report, model_evaluation, guidelines):
    report = []
    report.append(["Bias Analysis", ""])
    for feature, bias in bias_report.items():
        report.append([feature, json.dumps(bias)])

    report.append(["Model Evaluation", ""])
    if isinstance(model_evaluation, dict):
        report.append(["Accuracy", model_evaluation['accuracy']])
        report.append(["Confusion Matrix", json.dumps(model_evaluation['confusion_matrix'])])
    else:
        report.append(["Error", model_evaluation])

    report.append(["Ethical Guidelines Compliance", ""])
    for key, value in guidelines.items():
        report.append([key, value])

    return tabulate(report, headers=["Aspect", "Details"], tablefmt="grid")

def main():
    parser = argparse.ArgumentParser(description="AI Ethics Compliance Checker")
    parser.add_argument('--model', required=True, help="Path to the machine learning model file (pickle format).")
    parser.add_argument('--dataset', required=True, help="Path to the dataset file (CSV format).")
    parser.add_argument('--guidelines', required=True, help="Path to the ethical guidelines file (JSON format).")
    parser.add_argument('--output', help="Path to save the compliance report (optional).")

    args = parser.parse_args()

    try:
        model = load_model(args.model)
        dataset = load_dataset(args.dataset)
        guidelines = load_guidelines(args.guidelines)

        bias_report = check_bias(dataset)
        model_evaluation = evaluate_model(model, dataset)
        report = generate_report(bias_report, model_evaluation, guidelines)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Compliance report saved to {args.output}")
        else:
            print(report)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()