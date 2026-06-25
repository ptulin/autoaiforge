# LLM Code Review Assistant

## Description
The **LLM Code Review Assistant** is a command-line tool designed to analyze pull requests on GitHub or GitLab using an LLM (Large Language Model). It provides automated code review suggestions, identifying coding standards violations, potential bugs, and optimization opportunities. This tool is ideal for teams looking to streamline their code review processes.

## Features
- **Automatic Code Review for Pull Requests**: Analyze code changes in pull requests automatically.
- **Identify Coding Standards Violations and Bugs**: Get actionable feedback on potential issues.
- **Generate Suggestions and Explanations**: Receive detailed explanations and recommendations for improvement.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/llm_code_review_assistant.git
   cd llm_code_review_assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python llm_code_review_assistant.py --repo <repository_url> --pr <pull_request_id> --api-key <openai_api_key> [--output <output_file>]
```

### Example

```bash
python llm_code_review_assistant.py --repo https://github.com/user/repo --pr 123 --api-key your_openai_api_key --output review.json
```

- `--repo`: The URL of the GitHub or GitLab repository.
- `--pr`: The pull request ID to analyze.
- `--api-key`: Your OpenAI API key for accessing the LLM.
- `--output`: (Optional) Path to save the code review suggestions in JSON format.

## Example Output

```json
{
    "file_1": "Consider using a more descriptive variable name instead of 'x'.",
    "file_2": "This function can be optimized by using a list comprehension."
}
```

## Testing

To run the tests, use:

```bash
pytest test_llm_code_review_assistant.py
```

## Limitations
- The tool currently supports only GitHub and GitLab repositories.
- Requires an OpenAI API key to function.

## License
This project is licensed under the MIT License.
