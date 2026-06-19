# Rare Disease Diagnostic Assistant

## Overview
The Rare Disease Diagnostic Assistant is a CLI tool designed to assist healthcare professionals in identifying rare diseases. By inputting patient medical history and lab results in a structured format (CSV or JSON), the tool uses a pre-trained AI model to provide probabilistic diagnoses, ranked by confidence.

## Features
- Load patient data from CSV or JSON files.
- Use a pre-trained AI model to generate diagnostic predictions.
- Save diagnostic reports in JSON format.
- Generate visualizations of diagnostic confidence for each patient.

## Requirements
The following Python packages are required to run the tool:
- pandas
- numpy
- matplotlib
- scikit-learn
- joblib

Install the dependencies using pip:
```bash
pip install pandas numpy matplotlib scikit-learn joblib
```

## Usage
Run the CLI tool with the following command:
```bash
python rare_disease_diagnostic_assistant.py --input <input_file> --model <model_file> --output <output_file>
```

### Arguments
- `--input`: Path to the input patient data file (CSV or JSON).
- `--model`: Path to the pre-trained AI model file (Pickle format).
- `--output`: Path to save the diagnostic report (JSON format).

### Example
```bash
python rare_disease_diagnostic_assistant.py --input patient_data.csv --model ai_model.pkl --output diagnostic_report.json
```

## Testing
To run the tests, install `pytest`:
```bash
pip install pytest
```

Then execute the tests:
```bash
pytest test_rare_disease_diagnostic_assistant.py
```

## Notes
- Ensure the input data is properly formatted and matches the features expected by the AI model.
- The AI model must be a pre-trained `scikit-learn` model saved using `joblib`.
- The tool generates diagnostic visualizations for the top 5 probable diseases for each patient.

## License
This project is licensed under the MIT License.