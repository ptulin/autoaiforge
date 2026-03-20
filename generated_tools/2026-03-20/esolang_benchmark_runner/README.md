# EsoLang Benchmark Runner

## Description
The `esolang_benchmark_runner` is a CLI tool designed to execute EsoLang-Bench tasks on large language models (LLMs), measure their code generation accuracy for esoteric programming languages, and generate detailed performance reports. This tool is particularly useful for AI researchers and developers working with LLMs to benchmark their performance on esoteric language tasks.

## Features
- Executes EsoLang-Bench tasks using OpenAI models (e.g., GPT-4).
- Measures code generation accuracy and execution time.
- Supports output in JSON or CSV format.

## Requirements
- Python 3.7+
- Required Python packages:
  - `click`
  - `pandas`
  - `openai`

Install the required packages using pip:
```bash
pip install click pandas openai
```

## Usage
```bash
python esolang_benchmark_runner.py --model <MODEL_NAME> --language <LANGUAGE> --tasks <TASKS_FILE> --output <OUTPUT_FILE>
```

### Arguments
- `--model`: The OpenAI model to use (e.g., `gpt-4`).
- `--language`: The target esoteric programming language (e.g., `brainfuck`, `befunge`).
- `--tasks`: Path to the JSON file containing tasks. Each task should be a JSON object with a `prompt` key and an optional `expected_output` key.
- `--output`: Path to save the output metrics. Must have a `.json` or `.csv` extension.

### Example
1. Create a tasks file `tasks.json`:
    ```json
    [
        {
            "prompt": "Translate to brainfuck",
            "expected_output": "mocked_generated_code"
        }
    ]
    ```

2. Run the tool:
    ```bash
    python esolang_benchmark_runner.py --model gpt-4 --language brainfuck --tasks tasks.json --output output.json
    ```

3. Check the output file `output.json` for the results.

## Testing
To run the tests, install `pytest`:
```bash
pip install pytest
```

Run the tests:
```bash
pytest test_esolang_benchmark_runner.py
```

The tests include:
- Validating the tool generates correct JSON output.
- Handling invalid task file paths.
- Handling invalid output file extensions.

## Notes
- Ensure you have access to the OpenAI API and set up your API key in the environment variable `OPENAI_API_KEY`.
- The tool currently uses a simple string comparison to measure accuracy. For more complex benchmarking, consider implementing custom evaluation metrics.
