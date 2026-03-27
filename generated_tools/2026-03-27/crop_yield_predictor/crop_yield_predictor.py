import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from joblib import dump
import os

def preprocess_data(input_file):
    try:
        data = pd.read_csv(input_file)
        if data.empty:
            raise ValueError("Input CSV file is empty.")

        required_columns = ['soil_quality', 'temperature', 'rainfall', 'historical_yield']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")

        X = data[['soil_quality', 'temperature', 'rainfall']]
        y = data['historical_yield']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return X_scaled, y, scaler
    except Exception as e:
        raise ValueError(f"Error processing input file: {e}")

def train_model(X, y, model_type, **kwargs):
    if model_type == 'random_forest':
        model = RandomForestRegressor(**kwargs)
    elif model_type == 'neural_network':
        model = MLPRegressor(max_iter=500, **kwargs)
    else:
        raise ValueError("Unsupported model type. Choose 'random_forest' or 'neural_network'.")

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_val)
    mse = mean_squared_error(y_val, predictions)
    print(f"Validation Mean Squared Error: {mse}")

    return model

def predict_and_save(model, scaler, input_file, output_file):
    try:
        data = pd.read_csv(input_file)
        if data.empty:
            raise ValueError("Input CSV file is empty.")

        required_columns = ['soil_quality', 'temperature', 'rainfall']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")

        X = data[['soil_quality', 'temperature', 'rainfall']]
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)

        data['predicted_yield'] = predictions

        if output_file:
            data.to_csv(output_file, index=False)
            print(f"Predictions saved to {output_file}")
        else:
            print(data[['soil_quality', 'temperature', 'rainfall', 'predicted_yield']])
    except Exception as e:
        raise ValueError(f"Error during prediction or saving: {e}")

def main():
    parser = argparse.ArgumentParser(description="Crop Yield Predictor")
    parser.add_argument('--input', required=True, help="Path to input CSV file")
    parser.add_argument('--model', required=True, choices=['random_forest', 'neural_network'], help="Model type")
    parser.add_argument('--output', help="Path to save predictions (optional)")
    parser.add_argument('--save_model', help="Path to save trained model (optional)")
    parser.add_argument('--n_estimators', type=int, default=100, help="Number of trees for Random Forest (if applicable)")
    parser.add_argument('--hidden_layer_sizes', type=str, default="100", help="Hidden layer sizes for Neural Network (comma-separated, if applicable)")

    args = parser.parse_args()

    try:
        X, y, scaler = preprocess_data(args.input)

        if args.model == 'random_forest':
            model = train_model(X, y, 'random_forest', n_estimators=args.n_estimators)
        elif args.model == 'neural_network':
            hidden_layer_sizes = tuple(map(int, args.hidden_layer_sizes.split(',')))
            model = train_model(X, y, 'neural_network', hidden_layer_sizes=hidden_layer_sizes)

        if args.save_model:
            dump((model, scaler), args.save_model)
            print(f"Model and scaler saved to {args.save_model}")

        predict_and_save(model, scaler, args.input, args.output)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
