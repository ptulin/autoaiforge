# Prompt Compressor

Prompt Compressor is a Python library designed to help developers rewrite and compact prompts while retaining their semantic meaning. It leverages NLP techniques to remove redundancy, replace verbose wording with concise alternatives, and optionally compress numerical information. This tool is ideal for integrating into LLM pipelines to optimize prompt inputs.

## Features
- **Semantic-preserving prompt compression**: Compress prompts while maintaining their original meaning.
- **Configurable verbosity levels**: Choose between high, medium, or low verbosity for the output.
- **Easy integration**: Designed to be easily integrated into existing Python projects.

## Installation

Install the required dependencies using pip:

```bash
pip install transformers==4.33.3 nltk==3.8.1 python-Levenshtein==0.21.0
```

## Usage

### As a Library

You can use the `compress_prompt` function in your Python code:

```python
from prompt_compressor import compress_prompt

prompt = "This is a long and verbose prompt that needs to be rewritten in a concise manner."
compressed = compress_prompt(prompt, verbosity=1)
print(compressed)
```

### As a Command-Line Tool

You can also use Prompt Compressor as a command-line tool:

```bash
python prompt_compressor.py "This is a long and verbose prompt that needs to be rewritten in a concise manner." --verbosity 2
```

## Example

Input:
```
This is a long and verbose prompt that needs to be rewritten in a concise manner.
```

Output:
```
This is a concise prompt.
```

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_prompt_compressor.py
```

## License

This project is licensed under the MIT License.