import argparse
import json
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def analyze_model_weights(model: BaseEstimator) -> dict:
    if hasattr(model, 'coef_'):
        weights = model.coef_.tolist()
        return {'weights': weights}
    else:
        return {'weights': None}


def calculate_feature_importance(model: BaseEstimator) -> dict:
    if hasattr(model, 'feature_importances_'):
        feature_importances = model.feature_importances_.tolist()
        return {'feature_importances': feature_importances}
    else:
        return {'feature_importances': None}


def generate_explanation_report(model: BaseEstimator, input_data: pd.DataFrame) -> dict:
    weights = analyze_model_weights(model)
    feature_importances = calculate_feature_importance(model)
    return {**weights, **feature_importances}


def main():
    parser = argparse.ArgumentParser(description='AI Decision Explainer')
    parser.add_argument('--model_path', type=str, required=True)
    parser.add_argument('--input_data', type=str, required=True)
    parser.add_argument('--output_format', type=str, choices=['json', 'csv'], default='json')
    args = parser.parse_args()

    model = pd.read_pickle(args.model_path)
    input_data = pd.read_csv(args.input_data)

    explanation_report = generate_explanation_report(model, input_data)

    if args.output_format == 'json':
        print(json.dumps(explanation_report))
    elif args.output_format == 'csv':
        pd.DataFrame(explanation_report).to_csv('explanation_report.csv', index=False)

if __name__ == '__main__':
    main()