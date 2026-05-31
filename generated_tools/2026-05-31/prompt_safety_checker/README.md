# Prompt Safety Checker

## Overview
Prompt Safety Checker is a Python CLI tool designed to analyze AI model prompts for potentially harmful or inappropriate content before the input is fed to the model. It helps developers ensure that their systems are not generating harmful content due to problematic prompts.

## Features
- Analyze prompts for harmful or inappropriate content based on predefined safety rules.
- Detect negative sentiment in prompts.
- Interactive mode for real-time prompt analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd prompt_safety_checker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To check a single prompt:
```bash
python prompt_safety_checker.py check-prompt "Your prompt here"
```

To enable interactive mode:
```bash
python prompt_safety_checker.py check-prompt --interactive
```

### Example

```bash
$ python prompt_safety_checker.py check-prompt "This contains hate speech."
{'flagged_issues': ['contains hate speech'], 'suggestions': 'Consider rephrasing or removing flagged content.'}
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_prompt_safety_checker.py
```

All tests should pass successfully.

## Requirements
- Python 3.7+
- Typer

## Notes
This tool uses a mocked sentiment analysis function for testing purposes. In a production environment, you would replace this with a real sentiment analysis model or API.