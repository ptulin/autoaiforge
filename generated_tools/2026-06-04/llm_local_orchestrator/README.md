# llm_local_orchestrator

## Overview
`llm_local_orchestrator` is a Python CLI and library tool designed to simplify the management and inference of local Large Language Models (LLMs). It provides a consistent interface for running models with TensorSharp or PyTorch backends. The tool abstracts common setup tasks like hardware optimization, model loading, and tokenization, making it easier for developers to work with local LLMs.

## Features
- Load local LLM models and tokenizers.
- Run inference on input text using the loaded models.
- Support for PyTorch backend.
- CLI interface for easy usage.

## Installation
To install the required dependencies, run:

```bash
pip install torch transformers click
```

To install the testing dependencies, run:

```bash
pip install pytest
```

## Usage

### CLI Usage

Run the CLI tool with the following command:

```bash
python llm_local_orchestrator.py --model-path <path_to_model> --input "<input_text>" --device <device> --max-length <max_length>
```

- `--model-path`: Path to the local model.
- `--input`: Input text for the model.
- `--device`: Device to run the model on (e.g., `cuda` or `cpu`). Defaults to `cuda` if available, otherwise `cpu`.
- `--max-length`: Maximum length for generated text. Defaults to 128.

### Example

```bash
python llm_local_orchestrator.py --model-path ./gpt2 --input "Hello, world!" --device cpu --max-length 50
```

### Library Usage

You can also use the tool as a library in your Python code:

```python
from llm_local_orchestrator import load_model, run_inference

model_path = "./gpt2"
device = "cpu"
input_text = "Hello, world!"
max_length = 50

model, tokenizer = load_model(model_path, device)
result = run_inference(model, tokenizer, input_text, device, max_length)
print(result)
```

## Testing

To run the tests, use the following command:

```bash
pytest test_llm_local_orchestrator.py
```

The tests include:
- Verifying that the model and tokenizer load correctly.
- Testing the inference function with mocked inputs and outputs.
- Ensuring proper error handling for model loading and inference failures.

## License
This project is licensed under the MIT License.
