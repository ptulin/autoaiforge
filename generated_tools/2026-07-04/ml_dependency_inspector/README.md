# ML Dependency Inspector

ML Dependency Inspector is a Python CLI tool that scans AI/ML codebases for inefficient or insecure usages of popular libraries like TensorFlow, PyTorch, and Scikit-learn. It identifies deprecated methods, recommends modern alternatives, and detects configurations that may impact model performance or security.

## Features

- Detects deprecated methods such as `fit_transform` and `predict_proba`.
- Identifies insecure configurations, such as `shuffle=True` in training methods.
- Generates a detailed report in a tabular format.

## Installation

Install the required dependencies using pip:

```bash
pip install rich
```

## Usage

Run the tool from the command line by specifying the directory to analyze:

```bash
python ml_dependency_inspector.py --path /path/to/your/codebase
```

## Example Output

```
ML Dependency Inspector Report

+-------------------+---------------------+-------------------------+
| File              | Deprecated Methods | Insecure Configurations |
+-------------------+---------------------+-------------------------+
| /path/file1.py    | fit_transform      | None                    |
| /path/file2.py    | None               | shuffle=True in training|
+-------------------+---------------------+-------------------------+
```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_ml_dependency_inspector.py
```

Ensure all tests pass before using the tool in production.
