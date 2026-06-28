# Model Pruning Analyzer

## Overview
The Model Pruning Analyzer is a Python tool designed to help developers experiment with pruning techniques to reduce the size of local large language models (LLMs) while retaining acceptable accuracy levels. It provides detailed metrics to compare pre- and post-pruning model performance.

## Features
- Supports structured and unstructured pruning methods.
- Measures model size and inference speed before and after pruning.
- Outputs detailed metrics in JSON format.

## Installation
Ensure you have Python 3.7+ installed. Install the required dependencies:

```bash
pip install torch numpy
```

## Usage
Run the tool from the command line:

```bash
python model_pruning_analyzer.py --model_path <path_to_model> --method <structured|unstructured> --sparsity <sparsity_level> --output <output_file>
```

### Arguments
- `--model_path`: Path to the PyTorch model file.
- `--method`: Pruning method to use (`structured` or `unstructured`).
- `--sparsity`: Sparsity level (0 to 1).
- `--output`: Output file for metrics (default: `pruning_metrics.json`).

## Example
```bash
python model_pruning_analyzer.py --model_path model.pth --method structured --sparsity 0.5 --output metrics.json
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_model_pruning_analyzer.py
```

## License
This project is licensed under the MIT License.