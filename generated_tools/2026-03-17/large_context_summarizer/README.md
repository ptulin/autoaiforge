# Large Context Summarizer

## Overview
The Large Context Summarizer is a Python tool designed to summarize massive texts using AI models. It recursively generates summaries by breaking down large datasets into smaller chunks, summarizing them step-by-step, and producing concise outputs suitable for insights extraction or AI-ready inputs.

## Features
- Handles large text inputs by dividing them into manageable chunks.
- Recursively summarizes text to a specified depth and granularity.
- Supports both `.txt` and `.json` file formats for input and output.

## Installation
To use this tool, ensure you have Python 3.7 or later installed. Install the required dependencies:

```bash
pip install openai tiktoken
```

## Usage
Run the tool from the command line:

```bash
python large_context_summarizer.py --input <input_file> --depth <depth> --granularity <granularity> [--output <output_file>]
```

### Arguments
- `--input`: Path to the input `.txt` or `.json` file.
- `--depth`: Depth of recursive summarization (default: 3).
- `--granularity`: Number of chunks per summarization level (default: 5).
- `--output`: (Optional) Path to save the summarized output.

### Example
```bash
python large_context_summarizer.py --input example.txt --depth 2 --granularity 4 --output summary.txt
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_large_context_summarizer.py
```

## License
This project is licensed under the MIT License.