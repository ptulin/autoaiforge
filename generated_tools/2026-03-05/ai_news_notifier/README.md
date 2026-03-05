# AI News Notifier

## Description
AI News Notifier is a Python-based tool designed to monitor specific AI-related keywords or topics in news sources and alert developers in real time via email or desktop notifications. This ensures developers never miss important updates in the AI field.

## Features
- Fetch news articles from specified sources.
- Filter articles based on keywords.
- Notify users via email or desktop notifications.
- Configurable frequency for monitoring news.

## Installation
1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Create a configuration JSON file with the following structure:
   ```json
   {
       "keywords": ["OpenAI", "GPT"],
       "sources": ["https://example.com/news"],
       "notify_method": "email", // or "desktop"
       "email_config": {
           "smtp_server": "smtp.example.com",
           "smtp_port": 587,
           "username": "your_email@example.com",
           "password": "your_password",
           "to": "recipient_email@example.com"
       },
       "frequency": 10
   }
   ```
2. Run the tool:
   ```
   python ai_news_notifier.py --config path/to/config.json
   ```

## Testing
Run the tests using pytest:
```
pytest test_ai_news_notifier.py
```

## Requirements
- Python 3.7+
- plyer
- requests
- schedule

## License
MIT License