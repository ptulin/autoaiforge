# Agent Code Review

## Overview

`agent_code_review` is a CLI tool that uses an AI model to review Python code files for style, bugs, and optimization opportunities. It can also generate GitHub-style inline comments for suggested improvements, making it a valuable tool for automated code review pipelines.

## Features

- Analyze individual Python files or entire folders containing Python files.
- Generate AI-powered feedback for code style, bugs, and optimization.
- Save the review comments to a markdown file or display them in the terminal.

## Installation

Install the required dependencies:

```bash
pip install openai click pygments
```

## Usage

### Command-Line Interface

#### Analyze a Single File

```bash
python agent_code_review.py --file <path_to_file> --api-key <your_openai_api_key>
```

#### Analyze a Folder

```bash
python agent_code_review.py --folder <path_to_folder> --api-key <your_openai_api_key>
```

#### Save Output to a File

```bash
python agent_code_review.py --file <path_to_file> --api-key <your_openai_api_key> --output <output_file>
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_agent_code_review.py
```

## License

This project is licensed under the MIT License.
