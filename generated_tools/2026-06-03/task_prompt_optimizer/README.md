# Task Prompt Optimizer

## Description

Task Prompt Optimizer is a Python tool designed to help developers generate optimized prompts for AI coding agents. By analyzing specific coding tasks and iteratively refining prompts based on agent feedback, this tool ensures higher accuracy and efficiency in task execution. It simplifies interactions with coding agents, making them more effective and productive.

## Features

- **Iterative Prompt Refinement**: Refines prompts over multiple iterations for improved clarity and effectiveness.
- **Customizable Optimization Criteria**: Allows users to specify the number of refinement iterations.
- **Supports Multiple Agent APIs**: Built to work seamlessly with OpenAI's API.

## Installation

1. Clone the repository or download the `task_prompt_optimizer.py` file.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line with the following arguments:

```bash
python task_prompt_optimizer.py --api_key <your_openai_api_key> --input_prompt "<your_initial_prompt>" --iterations <number_of_iterations>
```

### Example

```bash
python task_prompt_optimizer.py --api_key myapikey --input_prompt "Write a Python script to sort a list" --iterations 5
```

## Output

The tool prints the optimized prompt to the console and logs the refinement process for review.

## Development

### Running Tests

To run the tests, use the following command:

```bash
pytest test_task_prompt_optimizer.py
```

### Mocking External Calls

All external calls to the OpenAI API are mocked during testing to ensure tests can run without network access.

## License

This project is licensed under the MIT License.
