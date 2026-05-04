# Email AI Sorter

## Overview

`email_ai_sorter` is a Python tool that connects to an email inbox, processes unread emails using OpenAI's GPT-3.5-turbo model to classify them into categories (e.g., 'work', 'personal', 'urgent'), and outputs the classification results. This tool is designed to help developers and users manage inbox overload by automatically categorizing emails.

## Features

- Connects to an email inbox using IMAP.
- Fetches unread emails from the inbox.
- Uses OpenAI's GPT-3.5-turbo model to classify emails into categories.
- Outputs the subject and category of each processed email.

## Requirements

- Python 3.7+
- `openai` Python package
- `python-dotenv` Python package

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd email_ai_sorter
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Run the script with the following command-line arguments:

```bash
python email_ai_sorter.py --imap-server <IMAP_SERVER> --email <EMAIL_ADDRESS> --password <EMAIL_PASSWORD> --api-key <OPENAI_API_KEY>
```

### Example:

```bash
python email_ai_sorter.py --imap-server imap.gmail.com --email user@gmail.com --password mypassword --api-key sk-xxxxxxxxxx
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_email_ai_sorter.py
```

The tests use mocking to simulate network calls, so no actual email server or OpenAI API calls are made during testing.

## License

This project is licensed under the MIT License.