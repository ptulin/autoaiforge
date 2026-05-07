# Claude Email Automation

## Overview
Claude Email Automation is a Python tool that integrates OpenAI's GPT-based API into email workflows. It analyzes email content and generates intelligent responses, summaries, or action items. This tool is ideal for developers looking to enhance productivity by automating email-related tasks.

## Features
- **Response Generation**: Draft professional responses to emails.
- **Summarization**: Summarize long email threads.
- **Action Items Extraction**: Extract actionable tasks from email content.

## Installation
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd claude_email_automation
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line with the following options:

```bash
python claude_email_automation.py --email-file <path_to_email_file> --mode <response|summary|action_items>
```

### Arguments
- `--email-file`: Path to the file containing the email content. If not provided, the tool will read from standard input.
- `--mode`: The mode of operation. Choose from:
  - `response`: Generate a professional response to the email.
  - `summary`: Summarize the email content.
  - `action_items`: Extract action items or to-do lists from the email.

### Example
1. To generate a response for an email stored in a file:
   ```bash
   python claude_email_automation.py --email-file email.txt --mode response
   ```
2. To summarize an email thread from standard input:
   ```bash
   python claude_email_automation.py --mode summary
   ```
   Paste the email content and press `Ctrl+D` (or `Ctrl+Z` on Windows) to end input.

## Testing
To run the tests, use `pytest`:

```bash
pytest test_claude_email_automation.py
```

The tests include:
- Validating the response generation.
- Validating the summarization.
- Validating the action items extraction.
- Handling empty email content.
- Handling invalid modes.
- Handling API errors.

## Requirements
- Python 3.7+
- `openai` package

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.