# Context Window Simulator

## Overview

The Context Window Simulator is a Python tool designed to help developers understand how a language model's context window truncates input prompts. By simulating the token limit of a language model, the tool visualizes which parts of the input prompt are retained and which are truncated. This allows developers to prioritize critical sections of their prompts.

## Features

- Simulate the token limit of a language model's context window.
- Visualize retained and truncated tokens using color-coded output.
- Identify critical sections of prompts to optimize for language model performance.

## Requirements

- Python 3.7+
- `rich` (for terminal-based visualization)
- `tiktoken` (for tokenization)

Install the required packages using pip:

```bash
pip install rich tiktoken
```

## Usage

Run the tool from the command line:

```bash
python context_window_simulator.py --input <path_to_input_file> --window <context_window_size>
```

### Arguments

- `--input`: Path to the input text file containing the prompt.
- `--window`: The context window size (e.g., 4096 for GPT-4).

### Example

Create a text file `prompt.txt` with the following content:

```
This is a sample prompt to test the context window simulator. It will help you understand how much of your input is retained and how much is truncated.
```

Run the tool:

```bash
python context_window_simulator.py --input prompt.txt --window 10
```

The output will display the retained tokens in green and the truncated tokens in red.

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_context_window_simulator.py
```

The test suite includes cases for:

- Ensuring prompts within the token limit are fully retained.
- Ensuring prompts exceeding the token limit are truncated.
- Handling file not found errors gracefully.
- Handling empty input files.
- Validating correct output for valid inputs.
