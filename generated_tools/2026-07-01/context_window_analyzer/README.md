# Context Window Analyzer

## Description

`context_window_analyzer` is a Python CLI tool that analyzes the token usage in long-context LLM (Large Language Model) inputs, visualizes token distribution, and highlights inefficiencies. It helps developers optimize prompts by identifying bottlenecks in token allocation, such as redundant or overly verbose sections.

## Features

- Analyze token usage in input text or JSON files.
- Identify inefficient sections with excessive token usage.
- Visualize token distribution as a histogram.

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages:

```bash
pip install matplotlib
```

## Usage

Run the script from the command line:

```bash
python context_window_analyzer.py --input <path_to_file> [--visualize]
```

### Arguments

- `--input`: Path to the input text or JSON file.
- `--visualize`: (Optional) Display a histogram of token distribution.

### Example

```bash
python context_window_analyzer.py --input example.json --visualize
```

## Testing

The tool includes a test suite using `pytest`. To run the tests:

1. Install `pytest`:

```bash
pip install pytest
```

2. Run the tests:

```bash
pytest test_context_window_analyzer.py
```

## Notes

- The tool uses a mock tokenizer for testing purposes. Replace the mock with the actual `tiktoken` library if available.
- Ensure input files are properly formatted (e.g., JSON files must contain a list of strings).

## License

This project is licensed under the MIT License.