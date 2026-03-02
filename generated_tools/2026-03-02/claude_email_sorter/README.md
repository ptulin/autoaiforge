# Claude Email Sorter

## Description
The Claude Email Sorter is a command-line tool designed to help users manage their email inboxes more efficiently. It connects to an email inbox using the IMAP protocol, fetches emails, and uses Claude AI's natural language processing capabilities to analyze and categorize emails based on user-defined rules. The categorized emails can be saved to a CSV file for further processing or reference.

## Features
- Connects to email inbox via IMAP.
- Uses Claude AI for email content analysis and classification.
- Allows user-defined rules for categorization.
- Outputs categorized emails to a CSV file.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/claude_email_sorter.git
   cd claude_email_sorter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file to store your IMAP credentials and Claude API key (optional):
   ```env
   IMAP_HOST=imap.example.com
   EMAIL=user@example.com
   PASSWORD=yourpassword
   CLAUDE_API_URL=https://api.claude.ai
   API_KEY=your_api_key
   ```

## Usage
Run the tool using the following command:
```bash
python claude_email_sorter.py --imap-host imap.example.com --email user@example.com --password secret123 --claude-api-url https://api.claude.ai --api-key your_api_key --output categorized_emails.csv
```

### Arguments
- `--imap-host`: The IMAP server host.
- `--email`: Your email address.
- `--password`: Your email account password.
- `--claude-api-url`: The URL for the Claude AI API.
- `--api-key`: Your Claude API key.
- `--output`: The output CSV file name (default: `output.csv`).

## Example
```bash
python claude_email_sorter.py --imap-host imap.gmail.com --email user@gmail.com --password mypassword --claude-api-url https://api.claude.ai --api-key myapikey --output sorted_emails.csv
```

## Testing
Run the tests using pytest:
```bash
pytest test_claude_email_sorter.py
```

## License
This project is licensed under the MIT License.