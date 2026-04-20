# AI Prompt Optimizer

## Description

`ai_prompt_optimizer` is a CLI tool designed to help developers fine-tune their prompts for AI models like GPT-5 and Claude 4.7. The tool generates permutations of a given prompt template, evaluates the responses from the AI models, and ranks the prompts based on their effectiveness using BLEU scores.

## Features
- Generate permutations of prompts based on variable inputs.
- Evaluate AI responses using BLEU scores.
- Support for GPT-5 and Claude 4.7 models.
- Save optimized prompts and their evaluations to a JSON file.

## Installation

Install the required dependencies:

```bash
pip install jinja2 nltk openai anthropic
```

## Usage

Run the tool from the command line:

```bash
python ai_prompt_optimizer.py \
    --prompt-template <path_to_template_file> \
    --variables <path_to_variables_json> \
    --reference <reference_text> \
    --model <gpt-5|claude-4.7> \
    --api-key <api_key> \
    --output <output_file>
```

### Arguments
- `--prompt-template`: Path to the file containing the prompt template (e.g., `"Explain {{topic}} in {{style}}"`).
- `--variables`: Path to the JSON file containing variables for the template (e.g., `{ "topic": ["AI", "ML"], "style": ["simple", "detailed"] }`).
- `--reference`: Reference text for evaluating the AI responses.
- `--model`: The AI model to use (`gpt-5` or `claude-4.7`).
- `--api-key`: API key for the selected AI model.
- `--output`: Path to save the optimized prompts and their evaluations in JSON format.

## Example

1. Create a prompt template file (`template.txt`):

```
Explain {{topic}} in {{style}}
```

2. Create a variables JSON file (`variables.json`):

```json
{
    "topic": ["AI", "ML"],
    "style": ["simple", "detailed"]
}
```

3. Run the tool:

```bash
python ai_prompt_optimizer.py \
    --prompt-template template.txt \
    --variables variables.json \
    --reference "This is a simple explanation of AI." \
    --model gpt-5 \
    --api-key YOUR_API_KEY \
    --output results.json
```

4. Check the output in `results.json`.

## Testing

Run the tests using `pytest`:

```bash
pytest test_ai_prompt_optimizer.py
```

## License

This project is licensed under the MIT License.