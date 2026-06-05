# Prompt Optimizer

## Description
Prompt Optimizer is a CLI tool designed to help AI developers systematically optimize prompts for large language models by testing variations and scoring their outputs. The tool allows users to define multiple prompt templates, supply test cases, and automatically evaluate and rank the effectiveness of each prompt using a custom scoring function.

## Features
- Generate prompt variations by replacing placeholders.
- Evaluate prompts using test cases and a custom scoring function.
- Save results in JSON or CSV format.

## Installation
Install the required Python packages:

```
pip install openai pandas numpy
```

## Usage
Run the tool using the following command:

```
python prompt_optimizer.py --prompt "Translate {text} to {language}" \
                           --test_cases test_cases.json \
                           --scorer scorer.py \
                           --output_format json \
                           --output_path results.json
```

### Arguments
- `--prompt`: Base prompt template with placeholders.
- `--test_cases`: Path to JSON file containing test cases.
- `--scorer`: Path to Python script defining scoring function.
- `--output_format`: Output format for results (`json` or `csv`).
- `--output_path`: Path to save the results.

## Testing
Run the tests using pytest:

```
pytest test_prompt_optimizer.py
```