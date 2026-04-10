# Prompt Debugger

## Overview
Prompt Debugger is a CLI tool designed to identify weaknesses in AI prompts by testing edge cases and generating diagnostic insights. It analyzes prompt responses for consistency, ambiguity, and sensitivity to wording changes.

## Features
- Generate edge cases for a given prompt.
- Analyze responses for consistency and ambiguity.
- Provide diagnostic insights and improvement suggestions.

## Installation

Install the required Python packages:

```bash
pip install openai typer pytest
```

## Usage

Run the tool from the command line:

```bash
python prompt_debugger.py --prompt "Write a story about a dragon." --model "gpt-3.5-turbo"
```

## Testing

Run the tests using pytest:

```bash
pytest test_prompt_debugger.py
```

## License

This project is licensed under the MIT License.
