# Error Pattern Analyzer

## Overview
Error Pattern Analyzer is a Python tool that uses AI models like OpenAI's GPT to analyze historical debugging logs or error traces. It identifies recurring error patterns and root causes, helping developers understand systemic issues in their codebases.

## Features
- Supports JSON and CSV log files.
- Uses OpenAI's GPT model for log analysis.
- Provides structured insights and preventive measures.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd error_pattern_analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python error_pattern_analyzer.py <file_path> <openai_api_key>
```

- `<file_path>`: Path to the debugging logs file (JSON or CSV).
- `<openai_api_key>`: Your OpenAI API key for GPT-based analysis.

### Example

```bash
python error_pattern_analyzer.py logs.json your_openai_api_key
```

## Testing

To run the tests, install `pytest` and run:

```bash
pytest test_error_pattern_analyzer.py
```

The tests include:
- Valid JSON log file analysis.
- Handling of empty log files.
- Handling of unsupported file formats.

## Requirements
- Python 3.7+
- `openai`
- `pandas`

## License
MIT License