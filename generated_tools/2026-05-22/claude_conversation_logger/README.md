# Claude Conversation Logger

## Description
The Claude Conversation Logger is a Python tool designed to facilitate structured logging of interactions with Claude AI. It allows developers to record and analyze conversations, tag messages by category, and export logs in CSV or JSON formats. This tool is particularly useful for monitoring AI-driven processes and auditing business automation reliability.

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script using the following command:

```bash
python claude_conversation_logger.py --prompt "Your prompt here" --tag "category" --export "logs.csv" --format "csv" --api_key "your_openai_api_key"
```

### Example

```bash
python claude_conversation_logger.py --prompt "What is the weather today?" --tag "weather" --export "weather_logs.json" --format "json" --api_key "your_openai_api_key"
```

## Features

- **Real-time logging**: Logs interactions with Claude AI in real-time.
- **Tagging and categorization**: Add tags or categories to each interaction for better organization.
- **Export options**: Save logs in CSV or JSON format for further analysis.

## Testing

Run the tests using pytest:

```bash
pytest test_claude_conversation_logger.py
```

## License

This project is licensed under the MIT License.