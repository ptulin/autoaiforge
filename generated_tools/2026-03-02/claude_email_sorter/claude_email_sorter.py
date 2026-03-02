import os
import csv
import imaplib
import email
import requests
import argparse
from email.header import decode_header
from dotenv import load_dotenv

def connect_to_imap(host, email_address, password):
    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(email_address, password)
        return mail
    except Exception as e:
        raise ConnectionError(f"Failed to connect to IMAP server: {e}")

def fetch_emails(mail):
    try:
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            raise ValueError("Failed to fetch emails")
        email_ids = messages[0].split()
        return email_ids
    except Exception as e:
        raise RuntimeError(f"Error fetching emails: {e}")

def parse_email(mail, email_id):
    try:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            raise ValueError(f"Failed to fetch email ID {email_id}")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                return subject, msg.get_payload(decode=True)
    except Exception as e:
        raise RuntimeError(f"Error parsing email ID {email_id}: {e}")

def classify_email(content, claude_api_url, api_key):
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"text": content}
        response = requests.post(claude_api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("category", "Uncategorized")
    except Exception as e:
        raise RuntimeError(f"Error classifying email: {e}")

def save_to_csv(output_file, email_categories):
    try:
        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Email Subject", "Category"])
            writer.writerows(email_categories)
    except Exception as e:
        raise IOError(f"Error saving to CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Email Sorter")
    parser.add_argument("--imap-host", required=True, help="IMAP server host")
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--password", required=True, help="Email password")
    parser.add_argument("--claude-api-url", required=True, help="Claude API URL")
    parser.add_argument("--api-key", required=True, help="Claude API key")
    parser.add_argument("--output", default="output.csv", help="Output CSV file")
    args = parser.parse_args()

    load_dotenv()

    imap_host = args.imap_host
    email_address = args.email
    password = args.password
    claude_api_url = args.claude_api_url
    api_key = args.api_key
    output_file = args.output

    mail = connect_to_imap(imap_host, email_address, password)
    email_ids = fetch_emails(mail)

    email_categories = []
    for email_id in email_ids:
        subject, content = parse_email(mail, email_id)
        category = classify_email(content.decode('utf-8'), claude_api_url, api_key)
        email_categories.append((subject, category))

    save_to_csv(output_file, email_categories)
    print(f"Emails categorized and saved to {output_file}")

if __name__ == "__main__":
    main()