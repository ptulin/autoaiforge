# Zero-Day Diff Checker

## Overview

The Zero-Day Diff Checker is a Python tool designed to compare two versions of a codebase and identify potential vulnerabilities introduced in new changes. It is ideal for use in CI pipelines or during code reviews.

## Features

- Compares two codebases and highlights differences.
- Identifies files that have been removed or modified.
- Provides AI-assisted analysis of code changes (mocked for testing).
- Outputs results in JSON or plain text format.

## Installation

Install the required dependencies:

```bash
pip install diff-match-patch
```

## Usage

Run the tool from the command line:

```bash
python zero_day_diff_checker.py <old_path> <new_path> [--output-format json|text]
```

### Arguments

- `old_path`: Path to the old version of the codebase.
- `new_path`: Path to the new version of the codebase.
- `--output-format`: Output format, either `json` or `text`. Defaults to `json`.

## Testing

To run the tests:

```bash
pytest test_zero_day_diff_checker.py
```

## License

This project is licensed under the MIT License.