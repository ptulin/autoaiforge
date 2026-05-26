# AI Ethics Compliance Checker

## Description
The AI Ethics Compliance Checker is a CLI tool designed to help developers and researchers analyze machine learning models and datasets for compliance with predefined ethical guidelines. It checks for bias in datasets, evaluates model performance, and generates a detailed compliance report.

## Features
- **Bias Analysis**: Detects potential bias in categorical features of datasets.
- **Model Evaluation**: Assesses the performance of machine learning models using accuracy and confusion matrix.
- **Ethical Guidelines Compliance**: Evaluates alignment with user-provided ethical guidelines.
- **Report Generation**: Outputs a detailed compliance report in a formatted text file or console.

## Installation
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage
Run the tool with the following command:

```bash
python ai_ethics_checker.py --model model.pkl --dataset data.csv --guidelines ethics.json --output report.txt
```

### Arguments
- `--model`: Path to the machine learning model file (pickle format).
- `--dataset`: Path to the dataset file (CSV format).
- `--guidelines`: Path to the ethical guidelines file (JSON format).
- `--output`: (Optional) Path to save the compliance report. If not provided, the report will be printed to the console.

### Example
```bash
python ai_ethics_checker.py --model model.pkl --dataset data.csv --guidelines ethics.json --output report.txt
```

## Testing
Run the tests using pytest:

```bash
pytest test_ai_ethics_checker.py
```

## License
This project is licensed under the MIT License.
