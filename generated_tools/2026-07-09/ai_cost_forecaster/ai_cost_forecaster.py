import argparse
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import os

def load_data(file_path):
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(data):
    if 'date' not in data.columns or 'cost' not in data.columns:
        raise ValueError("Input data must contain 'date' and 'cost' columns.")
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values('date', inplace=True)
    return data

def forecast_linear_regression(data, forecast_horizon):
    data['days'] = (data['date'] - data['date'].min()).dt.days
    X = data[['days']]
    y = data['cost']

    model = LinearRegression()
    model.fit(X, y)

    future_days = pd.DataFrame({'days': range(data['days'].max() + 1, data['days'].max() + 1 + forecast_horizon)})
    predictions = model.predict(future_days)

    return future_days['days'], predictions

def forecast_arima(data, forecast_horizon):
    model = ARIMA(data['cost'], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_horizon)
    return forecast

def plot_forecast(data, forecast_days, forecast_values, method):
    plt.figure(figsize=(10, 6))
    plt.plot(data['date'], data['cost'], label='Historical Data')

    if method == 'linear':
        future_dates = data['date'].min() + pd.to_timedelta(forecast_days, unit='D')
    else:
        future_dates = pd.date_range(start=data['date'].iloc[-1], periods=len(forecast_values)+1, freq='D')[1:]

    plt.plot(future_dates, forecast_values, label='Forecast', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Cost')
    plt.title(f'Cost Forecast ({method.capitalize()})')
    plt.legend()
    plt.grid()
    plt.show()

def save_forecast_to_csv(forecast_days, forecast_values, output_file):
    df = pd.DataFrame({'day': forecast_days, 'predicted_cost': forecast_values})
    df.to_csv(output_file, index=False)

def main():
    parser = argparse.ArgumentParser(description="AI Cost Forecaster")
    parser.add_argument('--input-file', required=True, help="Path to the input file (CSV or JSON).")
    parser.add_argument('--forecast-horizon', type=int, default=7, help="Number of days to forecast.")
    parser.add_argument('--method', choices=['linear', 'arima'], default='linear', help="Forecasting method to use.")
    parser.add_argument('--output-file', help="Optional path to save the forecast as a CSV file.")

    args = parser.parse_args()

    try:
        data = load_data(args.input_file)
        data = preprocess_data(data)

        if args.method == 'linear':
            forecast_days, forecast_values = forecast_linear_regression(data, args.forecast_horizon)
        elif args.method == 'arima':
            forecast_values = forecast_arima(data, args.forecast_horizon)
            forecast_days = range(1, args.forecast_horizon + 1)

        plot_forecast(data, forecast_days, forecast_values, args.method)

        if args.output_file:
            save_forecast_to_csv(forecast_days, forecast_values, args.output_file)
            print(f"Forecast saved to {args.output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()