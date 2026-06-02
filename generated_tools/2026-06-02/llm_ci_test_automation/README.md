# LLM-Integrated CI Test Automation Library

## Description
The **LLM-Integrated CI Test Automation Library** is a Python tool designed to integrate seamlessly with CI/CD pipelines. It automates the generation of test cases using OpenAI's language models by analyzing code changes in pull requests. This tool fetches pull request diffs, processes them with a customizable prompt, and outputs structured test cases that can be reviewed or directly executed.

## Features
- **Seamless CI/CD Integration**: Easily integrates into your CI/CD workflows.
- **Automated Test Case Generation**: Automatically generates test cases based on code changes in pull requests.
- **Customizable Prompts**: Tailor prompts to suit your testing requirements.
- **Output in Structured Format**: Test cases are returned as Python data structures for easy consumption.

## Installation
To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Example Usage in Code
```python
from llm_ci_test_automation import generate_test_cases

test_cases = generate_test_cases(
    repo_url='github.com/user/repo', 
    pr_id=42, 
    token='your_github_token', 
    openai_api_key='your_openai_api_key'
)
print(test_cases)
```

### CLI Usage
```bash
python llm_ci_test_automation.py \
    --repo_url github.com/user/repo \
    --pr_id 42 \
    --github_token your_github_token \
    --openai_api_key your_openai_api_key
```

## Example Output
```python
[
    {
        "name": "test_case_1",
        "code": "assert 1 == 1"
    },
    {
        "name": "test_case_2",
        "code": "assert my_function(2) == 4"
    }
]
```

## Requirements
- Python 3.7+
- `openai==0.27.8`
- `requests==2.31.0`
- `pytest==7.4.2`

## License
This project is licensed under the MIT License.
