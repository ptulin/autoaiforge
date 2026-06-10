# Misidentification Analyzer

## Overview
The Misidentification Analyzer is a Python library designed to help developers analyze misidentifications made by AI models. It provides tools for confusion matrix analysis, error clustering, and visual inspection of problematic data points. This tool is particularly useful for identifying patterns of errors that could lead to real-world harm.

## Features
- Generate confusion matrices for model predictions.
- Create classification reports with precision, recall, and F1-score.
- Identify and cluster misclassified data points.
- Visualize confusion matrices using heatmaps.

## Installation
To install the required dependencies, run:

```bash
pip install numpy matplotlib seaborn scikit-learn
```

## Usage
The tool can be used as a standalone script or as a library in your Python projects.

### Command-Line Usage
Run the script from the command line with the following arguments:

```bash
python misidentification_analyzer.py --predictions <path_to_predictions_file> \
                                     --true_labels <path_to_true_labels_file> \
                                     [--metadata <path_to_metadata_file>] \
                                     [--n_clusters <number_of_clusters>]
```

- `--predictions`: Path to a file containing model predictions (comma-separated values).
- `--true_labels`: Path to a file containing true labels (comma-separated values).
- `--metadata`: (Optional) Path to a JSON file containing metadata for each data point.
- `--n_clusters`: (Optional) Number of clusters for error clustering (default: 3).

### Library Usage
You can also use the `analyze_errors` function directly in your Python code:

```python
from misidentification_analyzer import analyze_errors

predictions = [0, 1, 2, 2, 0]
true_labels = [0, 1, 1, 2, 0]
metadata = [
    {"age": 25, "gender": "M"},
    {"age": 30, "gender": "F"},
    {"age": 22, "gender": "M"},
    {"age": 28, "gender": "F"},
    {"age": 35, "gender": "M"},
]

result = analyze_errors(predictions, true_labels, metadata, n_clusters=2, output_json=False)
print(result)
```

## Testing
To run the tests, install `pytest` and execute the test file:

```bash
pip install pytest
pytest test_misidentification_analyzer.py
```

## License
This project is licensed under the MIT License.
