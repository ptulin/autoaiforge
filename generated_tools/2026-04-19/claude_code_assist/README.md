# Claude Code Assist

Claude Code Assist is a command-line tool that integrates with Claude Code API to provide real-time code suggestions, debugging, and annotations directly in supported IDEs. It acts as an intermediary between the developer's IDE and the Claude Code API.

## Features
- Suggest improvements to your code.
- Debug code and identify issues.
- Annotate code with explanations.

## Installation

Install the required Python packages:

```bash
pip install openai rich
```

## Usage

Run the tool using the following command:

```bash
python claude_code_assist.py --file <path_to_code_file> --action <suggest|debug|annotate> --api_key <your_openai_api_key> [--output <output_file>]
```

### Arguments
- `--file`: Path to the code file to process.
- `--action`: Action to perform on the code. Options are `suggest`, `debug`, or `annotate`.
- `--api_key`: Your OpenAI API key.
- `--output`: (Optional) Path to save the processed code.

### Example

```bash
python claude_code_assist.py --file example.py --action debug --api_key YOUR_API_KEY --output result.py
```

## Testing

To run the tests:

```bash
pytest test_claude_code_assist.py
```

## License

MIT License