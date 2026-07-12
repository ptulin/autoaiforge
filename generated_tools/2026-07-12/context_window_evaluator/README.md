# Context Window Evaluator

## Overview
The Context Window Evaluator is a Python tool designed to analyze prompt datasets for large language models (LLMs). It evaluates token density, redundancy, and truncation risks to help developers optimize prompt design and maximize information fit within the LLM's context window.

## Features
- Analyze token usage, redundancy, and truncation risks for individual prompts.
- Process multiple prompts from text or JSON files.
- Generate a detailed report in the terminal or save it as a JSON file.

## Requirements
- Python 3.8+
- `tiktoken`
- `nltk`
- `rich`

## Installation
Install the required dependencies using pip:

```bash
pip install tiktoken nltk rich
```

## Usage

### Command Line Interface
Run the tool from the command line:

```bash
python context_window_evaluator.py --input <file1> <file2> --output <output_file>
```

- `--input`: One or more input files (text or JSON) containing prompts to analyze.
- `--output`: (Optional) Path to save the analysis report as a JSON file.

### Example
Analyze a file `prompts.txt` and save the report to `report.json`:

```bash
python context_window_evaluator.py --input prompts.txt --output report.json
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_context_window_evaluator.py
```

The tests include:
- Unit tests for analyzing individual prompts.
- Unit tests for analyzing files with multiple prompts.
- Unit tests for generating reports and saving them to a file.

## License
This project is licensed under the MIT License.