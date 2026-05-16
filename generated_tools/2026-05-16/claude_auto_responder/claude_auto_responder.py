import json
import logging
import os
from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel, ValidationError
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import argparse

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Scenario(BaseModel):
    keyword: str
    response_template: str

class Config(BaseModel):
    gmail_credentials_file: str
    scenarios: List[Scenario]
    anthropic_api_key: str

def load_config(config_path: str) -> Config:
    try:
        with open(config_path, 'r') as file:
            data = json.load(file)
            return Config(**data)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_path}")
        raise
    except ValidationError as e:
        logging.error(f"Invalid config format: {e}")
        raise

def get_gmail_service(credentials_file: str):
    try:
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(credentials_file, ['https://www.googleapis.com/auth/gmail.modify'])
        service = build('gmail', 'v1', credentials=creds)
        return service
    except FileNotFoundError:
        logging.error(f"Gmail credentials file not found: {credentials_file}")
        raise
    except HttpError as error:
        logging.error(f"An error occurred with the Gmail API: {error}")
        raise

def fetch_unread_emails(service):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        logging.error(f"An error occurred while fetching emails: {error}")
        return []

def get_email_content(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "")
        body = ""
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                body = part.get('body', {}).get('data', '')
                break
        return subject, body
    except HttpError as error:
        logging.error(f"An error occurred while fetching email content: {error}")
        return "", ""

def generate_response(api_key: str, prompt: str) -> str:
    try:
        client = Anthropic(api_key=api_key)
        response = client.completions.create(
            model="claude-v1",
            prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
            max_tokens_to_sample=300
        )
        return response.completion.strip()
    except Exception as e:
        logging.error(f"An error occurred while generating response: {e}")
        return ""

def send_email(service, to, subject, body):
    try:
        from email.mime.text import MIMEText
        import base64

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    except HttpError as error:
        logging.error(f"An error occurred while sending email: {error}")

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Claude Auto Responder")
    parser.add_argument('--config', required=True, help="Path to the configuration JSON file")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        service = get_gmail_service(config.gmail_credentials_file)
        messages = fetch_unread_emails(service)

        for message in messages:
            message_id = message['id']
            subject, body = get_email_content(service, message_id)

            for scenario in config.scenarios:
                if scenario.keyword.lower() in body.lower():
                    prompt = scenario.response_template.replace("{{customer_message}}", body)
                    response = generate_response(config.anthropic_api_key, prompt)
                    send_email(service, "customer@example.com", f"Re: {subject}", response)
                    break

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
