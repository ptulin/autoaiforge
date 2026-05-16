# Claude Auto Responder

Claude Auto Responder is a Python CLI tool that integrates with Anthropic's Claude to provide automated customer support via email. Users can define common customer scenarios and responses, allowing small businesses to streamline email support while maintaining a professional touch.

## Features
- Automatically fetch unread emails from a Gmail account.
- Analyze email content to match predefined customer scenarios.
- Generate AI-powered responses using Anthropic's Claude.
- Send automated replies to customers via Gmail.

## Requirements
- Python 3.8+
- `google-api-python-client`
- `pydantic`
- `anthropic`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/claude_auto_responder.git
   cd claude_auto_responder
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Create a JSON configuration file with the following structure:

```json
{
  "gmail_credentials_file": "path/to/credentials.json",
  "scenarios": [
    {
      "keyword": "refund",
      "response_template": "Hello, regarding your refund: {{customer_message}}"
    }
  ],
  "anthropic_api_key": "your_anthropic_api_key"
}
```

- `gmail_credentials_file`: Path to your Gmail API credentials file.
- `scenarios`: List of scenarios with keywords and response templates.
- `anthropic_api_key`: Your API key for Anthropic's Claude.

## Usage
Run the tool using the following command:

```bash
python claude_auto_responder.py --config path/to/config.json
```

## Testing
To run the tests, use `pytest`:

```bash
pytest test_claude_auto_responder.py
```

## License
MIT License
