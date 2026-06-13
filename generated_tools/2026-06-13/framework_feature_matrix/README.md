# Framework Feature Matrix

This Python tool generates a comparison table of features supported by various open-source AI frameworks. It scrapes official documentation or uses pre-defined metadata to summarize capabilities like model serialization, hardware support, and built-in optimization algorithms.

## Features
- Compare features of popular AI frameworks like TensorFlow, PyTorch, and JAX.
- Fetch framework metadata from official documentation.
- Output the feature matrix in JSON, CSV, or Markdown format.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the script using the command line:

```bash
python framework_feature_matrix.py --frameworks tensorflow pytorch --output json --output-file output.json
```

### Arguments
- `--frameworks`: List of frameworks to compare (e.g., `tensorflow`, `pytorch`, `jax`).
- `--output`: Output format (`json`, `csv`, or `markdown`).
- `--output-file`: Path to the output file.

## Example

Generate a Markdown table comparing TensorFlow and PyTorch features:

```bash
python framework_feature_matrix.py --frameworks tensorflow pytorch --output markdown --output-file feature_matrix.md
```

## Testing

Run the tests using pytest:

```bash
pytest test_framework_feature_matrix.py
```

## Requirements

- Python 3.7+
- `beautifulsoup4`
- `requests`
- `tabulate`
- `pytest`

## License

This project is licensed under the MIT License.