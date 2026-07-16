# LLM Prompt Optimizer

## Description
The LLM Prompt Optimizer is a Python tool designed to help developers optimize prompts for open-weight large language models. It systematically generates variations of a base prompt, evaluates them using a user-defined scoring function, and identifies the best-performing prompt. This tool is ideal for developers working on natural language processing tasks who want to maximize the effectiveness of their prompts.

## Features
- Generate systematic variations of a base prompt.
- Evaluate prompt variations using a specified language model.
- Score responses using a custom scoring function provided by the user.
- Identify and return the best-performing prompt.
- Save evaluation reports to a file or display them in the console.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/llm_prompt_optimizer.git
   cd llm_prompt_optimizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

```bash
python llm_prompt_optimizer.py --model <model_name> --base_prompt <base_prompt> --scoring_script <path_to_scoring_script> [--output_file <output_file>]
```

#### Arguments:
- `--model`: Name of the language model to use (e.g., `gpt-3`, `inkling-975b`).
- `--base_prompt`: The base prompt to optimize.
- `--scoring_script`: Path to a Python script containing a `score_prompt` function.
- `--output_file` (optional): File path to save the evaluation report.

### Example

```bash
python llm_prompt_optimizer.py --model inkling-975b --base_prompt 'Translate to French:' --scoring_script score.py --output_file results.json
```

### Scoring Script Example
The scoring script must define a `score_prompt` function that takes two arguments: `prompt` and `response`. For example:

```python
def score_prompt(prompt, response):
    # Example scoring function: longer responses get higher scores
    return len(response)
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_prompt_optimizer.py
```

## License
MIT License