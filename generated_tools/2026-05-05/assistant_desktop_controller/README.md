# Assistant Desktop Controller

## Description

Assistant Desktop Controller is a CLI tool that uses natural language commands to control desktop applications and perform common tasks. It connects to AI assistants like OpenAI's GPT to interpret commands and uses Python libraries to execute these tasks, such as creating files or scheduling events.

## Features

- Parse natural language commands using OpenAI's GPT.
- Execute tasks like creating files and scheduling events.
- Extendable for additional functionalities.

## Installation

Install the required Python packages:

```bash
pip install openai schedule
```

## Usage

Run the tool with a natural language command:

```bash
python assistant_desktop_controller.py --command "Create a file"
```

## Testing

Run the tests using pytest:

```bash
pytest test_assistant_desktop_controller.py
```

## Limitations

- Email sending functionality is not implemented.
- Requires an OpenAI API key to function.

## License

MIT License