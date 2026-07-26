# LLM Micro Optimizer

## Overview

The LLM Micro Optimizer is a Python tool designed to fine-tune large language models (LLMs) for deployment on microcontrollers. It reduces the size and complexity of models while maintaining their performance by applying techniques such as:

- **Weight Pruning**: Removes redundant weights from the model.
- **Embedding Compression**: Compresses embeddings to reduce memory usage.
- **Distillation**: Applies teacher-student training techniques using a dataset.

## Features

- Supports optimization levels: `low` and `high`.
- Optional distillation using a dataset.
- Saves the optimized model to a specified path.

## Installation

Install the required dependencies using pip:

```bash
pip install torch transformers scipy
```

## Usage

Run the tool from the command line:

```bash
python llm_micro_optimizer.py --model_path <path_to_model> \
                              --optimization_level <low|high> \
                              --save_path <path_to_save_model> \
                              [--distillation_dataset <path_to_dataset>]
```

### Arguments

- `--model_path`: Path to the PyTorch model file to optimize.
- `--optimization_level`: Optimization level (`low` or `high`).
- `--save_path`: Path to save the optimized model.
- `--distillation_dataset`: (Optional) Path to the dataset for distillation.

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_micro_optimizer.py
```

The tests cover the following:

- Weight pruning functionality.
- Embedding compression functionality.
- Full model optimization workflow.

## License

This project is licensed under the MIT License.