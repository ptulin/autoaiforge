# Token Efficiency Optimizer

## Overview
The Token Efficiency Optimizer is a Python library designed to optimize token handling in LLM workflows. It dynamically adjusts token limits and recommends efficient configurations for high-token operations, preventing out-of-memory errors and enhancing throughput for applications with large inputs.

## Features
- Splits input text into manageable token batches based on memory constraints.
- Prevents out-of-memory errors by dynamically adjusting token limits.
- Compatible with Hugging Face tokenizers.

## Installation
To use this tool, install the required dependencies:

```bash
pip install numpy transformers
```

## Usage
Run the script from the command line:

```bash
python token_efficiency_optimizer.py "Your input text here" --max_memory 8 --tokenizer bert-base-uncased
```

### Arguments
- `input_text`: The raw text input to optimize.
- `--max_memory`: Maximum memory in GB (default: 8).
- `--tokenizer`: Pretrained tokenizer model name (e.g., 'bert-base-uncased').

## Example
```bash
python token_efficiency_optimizer.py "This is a test input." --max_memory 4 --tokenizer bert-base-uncased
```

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_token_efficiency_optimizer.py
```

## License
This project is licensed under the MIT License.