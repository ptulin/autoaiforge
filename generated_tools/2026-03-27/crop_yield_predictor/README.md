# Crop Yield Predictor

## Overview
The Crop Yield Predictor is a Python-based tool that uses machine learning models to predict crop yields based on input features such as soil quality, climate data, and historical yield data. This tool is designed to assist AI developers in building and testing prediction models for agricultural datasets, promoting smart farming solutions.

## Features
- Preprocess input CSV data containing soil quality, temperature, rainfall, and historical yield.
- Train machine learning models (Random Forest or Neural Network) to predict crop yields.
- Save trained models and scalers for future use.
- Predict crop yields and save predictions to an output CSV file.

## Requirements
- Python 3.7+
- pandas
- numpy
- scikit-learn
- joblib
- pytest (for testing)

## Installation
Install the required Python packages using pip:

```bash
pip install pandas numpy scikit-learn joblib pytest
```

## Usage
Run the script from the command line with the following arguments:

```bash
python crop_yield_predictor.py --input <input_csv> --model <model_type> [--output <output_csv>] [--save_model <model_file>] [--n_estimators <num_trees>] [--hidden_layer_sizes <sizes>]
```

### Arguments
- `--input`: Path to the input CSV file containing the data.
- `--model`: Model type to use for training (`random_forest` or `neural_network`).
- `--output`: (Optional) Path to save the predictions as a CSV file.
- `--save_model`: (Optional) Path to save the trained model and scaler.
- `--n_estimators`: (Optional) Number of trees for the Random Forest model (default: 100).
- `--hidden_layer_sizes`: (Optional) Comma-separated hidden layer sizes for the Neural Network model (default: "100").

### Input File Format
The input CSV file must contain the following columns:
- `soil_quality`
- `temperature`
- `rainfall`
- `historical_yield`

### Example
#### Training a Random Forest Model
```bash
python crop_yield_predictor.py --input data.csv --model random_forest --n_estimators 200 --output predictions.csv --save_model model.joblib
```

#### Training a Neural Network Model
```bash
python crop_yield_predictor.py --input data.csv --model neural_network --hidden_layer_sizes 100,50 --output predictions.csv --save_model model.joblib
```

## Testing
Run the tests using pytest:

```bash
pytest test_crop_yield_predictor.py
```

The test suite includes tests for data preprocessing, model training, and prediction functionality. All tests are self-contained and use mocking to avoid external dependencies.

## License
This project is licensed under the MIT License.