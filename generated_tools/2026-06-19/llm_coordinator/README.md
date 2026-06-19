# LLM Coordinator

## Overview

LLM Coordinator is a Python CLI tool that orchestrates workflows between multiple large language models (LLMs). It allows AI developers to define roles and communication strategies for each model, enabling collaborative pipelines such as summarization, sentiment analysis, and more.

## Features

- Define workflows with multiple steps, each specifying a model, task, and API key.
- Automatically handle errors and missing fields in configuration.
- Log execution progress and errors.

## Installation

Install the required dependencies:

```bash
pip install langchain
```

## Usage

Run the tool with a JSON configuration file:

```bash
python llm_coordinator.py --config path/to/config.json
```

### Configuration File Format

The configuration file should be a JSON file with the following structure:

```json
{
  "steps": [
    {
      "name": "step1",
      "model": "text-davinci-003",
      "task": "Summarize this text.",
      "api_key": "your_openai_api_key"
    }
  ]
}
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_coordinator.py
```

## License

This project is licensed under the MIT License.