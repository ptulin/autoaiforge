# Token Usage Profiler

## Overview
The Token Usage Profiler is a command-line tool designed to analyze and profile token usage in prompts sent to language models. It identifies high-frequency tokens, calculates token distribution across prompt sections, and highlights areas for optimization. This helps developers reduce model costs and improve performance by crafting more efficient prompts.

## Features
- Analyze token usage in a given text prompt.
- Identify high-frequency tokens.
- Provide optimization suggestions to reduce token usage.
- Generate a tabular report summarizing the analysis.

## Requirements
- Python 3.7+
- `tabulate`
- `tiktoken`

Install the required packages using pip:
```bash
pip install tabulate tiktoken
```

## Installation
Save the script `token_usage_profiler.py` to your local machine.

## Usage
Run the script from the command line with the following syntax:
```bash
python token_usage_profiler.py --input <path_to_prompt_file>
```

### Example
Suppose you have a file `prompt.txt` with the following content:
```
This is a test prompt. This is a test prompt.
```
Run the tool as follows:
```bash
python token_usage_profiler.py --input prompt.txt
```

The output will be a tabular report like this:
```
+-------------------------+------------------------------------------------+
| Metric                 | Value                                          |
+-------------------------+------------------------------------------------+
| Total Tokens           | 10                                             |
| High-Frequency Tokens  |                                                |
| Token ID 1             | 4                                              |
| Token ID 2             | 3                                              |
| Token ID 3             | 3                                              |
| Optimization Suggestions |                                                |
| -                      | High-frequency tokens detected. Consider       |
|                        | rephrasing to reduce repetition.              |
+-------------------------+------------------------------------------------+
```

## Testing
To run the tests, install `pytest`:
```bash
pip install pytest
```

Run the tests using the following command:
```bash
pytest test_token_usage_profiler.py
```

The tests include:
- Validating analysis of a valid prompt file.
- Handling of empty input files.
- Handling of non-existent files.
- Generating a report from analysis results.

All tests should pass successfully.
