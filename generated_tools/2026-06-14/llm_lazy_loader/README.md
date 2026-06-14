# LLM Lazy Loader

## Overview

LLM Lazy Loader is a lightweight Python library that allows developers to load large language models in a lazy manner, enabling parts of the model to be loaded and swapped out of memory dynamically during inference. This is especially useful for running large models on devices with limited RAM.

## Features

- Lazy loading of Hugging Face models and tokenizers.
- Memory usage checks to ensure models are loaded only when sufficient memory is available.
- Easy-to-use API for loading models and performing inference.

## Installation

Install the required dependencies:

```bash
pip install torch transformers psutil
```

## Usage

Run the script from the command line:

```bash
python llm_lazy_loader.py <model_name> --memory_limit <memory_limit_in_MB>
```

Example:

```bash
python llm_lazy_loader.py gpt2 --memory_limit 2000
```

### Programmatic Usage

```python
from llm_lazy_loader import LazyLoader

loader = LazyLoader("gpt2", memory_limit=2000)
try:
    loader.load()
    output = loader.generate("Hello, world!")
    print(output)
except MemoryError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_lazy_loader.py
```

## License

This project is licensed under the MIT License.