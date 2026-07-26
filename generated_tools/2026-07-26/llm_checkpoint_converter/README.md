# LLM Checkpoint Converter

## Overview

The LLM Checkpoint Converter is a Python utility that allows you to convert model checkpoints between PyTorch and TensorFlow formats. This enables seamless interoperability and deployment of models across various ecosystems.

## Features

- Convert PyTorch checkpoints to TensorFlow SavedModel format.
- Convert TensorFlow checkpoints to PyTorch format.
- Validate input files and handle errors gracefully.

## Requirements

- Python 3.7+
- Required Python packages:
  - `torch`
  - `tensorflow`
  - `transformers`

Install the required packages using pip:

```bash
pip install torch tensorflow transformers
```

## Usage

Run the script from the command line with the following arguments:

```bash
python llm_checkpoint_converter.py --input <input_checkpoint> --output_format <pytorch|tensorflow> --output <output_checkpoint>
```

### Arguments

- `--input`: Path to the input checkpoint file.
- `--output_format`: Target format for the conversion (`pytorch` or `tensorflow`).
- `--output`: Path to save the converted checkpoint.

### Example

Convert a PyTorch checkpoint to TensorFlow:

```bash
python llm_checkpoint_converter.py --input model.pt --output_format tensorflow --output model_tf
```

Convert a TensorFlow checkpoint to PyTorch:

```bash
python llm_checkpoint_converter.py --input model_tf --output_format pytorch --output model.pt
```

## Testing

To run the tests, install `pytest` and run the following command:

```bash
pytest test_llm_checkpoint_converter.py
```

The tests include:

1. Conversion from PyTorch to TensorFlow.
2. Conversion from TensorFlow to PyTorch.
3. Handling invalid output formats.
4. Handling missing input files.

## License

This project is licensed under the MIT License.