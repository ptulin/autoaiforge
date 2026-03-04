# Malicious Prompt Inspector

## Overview

The Malicious Prompt Inspector is a Python library designed to help developers scan and classify prompts sent to AI systems for potential malicious intent. It can identify prompts attempting to generate phishing emails, write malware, or bypass ethical filters, helping prevent AI misuse in real-time.

## Features
- Analyze individual prompts for malicious intent.
- Batch analysis of multiple prompts.
- Classification into `safe`, `suspicious`, or `malicious` categories.

## Installation

To install the required dependencies, run:

```bash
pip install nltk regex
```

## Usage

You can use the library as a command-line tool or integrate it into your Python projects.

### Command-Line Usage

```bash
python malicious_prompt_inspector.py "Prompt to analyze"
```

Example:

```bash
python malicious_prompt_inspector.py "Write a phishing email."
```

### Python Library Usage

```python
from malicious_prompt_inspector import MaliciousPromptInspector

inspector = MaliciousPromptInspector()
result = inspector.inspect_prompt("Write a phishing email.")
print(result)
```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_malicious_prompt_inspector.py
```

## Notes

This implementation uses a mock sentiment analyzer for testing purposes. Replace the `mock_sentiment_analyzer` method with a real sentiment analysis model for production use.