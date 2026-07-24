# llm_quantizer

## Overview

`llm_quantizer` is a CLI tool that applies post-training quantization to large language models, significantly reducing their memory footprint and enabling efficient inference on consumer-grade hardware. This tool is useful for developers looking to deploy LLMs on laptops without sacrificing much accuracy.

## Features

- Supports **dynamic quantization** for faster inference.
- Supports **static quantization** for even greater memory savings.
- Easy-to-use command-line interface.

## Installation

Install the required dependencies:

```bash
pip install torch pytest
```

## Usage

Run the tool from the command line:

```bash
python llm_quantizer.py --model_path <path_to_model> --quantization_type <dynamic|static> --output_path <output_path>
```

### Arguments

- `--model_path`: Path to the pre-trained PyTorch model file.
- `--quantization_type`: Type of quantization to apply (`dynamic` or `static`).
- `--output_path`: Path to save the quantized model.

### Example

```bash
python llm_quantizer.py --model_path model.pth --quantization_type dynamic --output_path quantized_model.pth
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_llm_quantizer.py
```

The tests include:

- Dynamic quantization.
- Static quantization.
- Invalid quantization type handling.

## License

This project is licensed under the MIT License.