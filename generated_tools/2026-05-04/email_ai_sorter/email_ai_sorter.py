import os
import imaplib
import email
from email.header import decode_header
import argparse
from openai import ChatCompletion
from dotenv import load_dotenv
import openai

def connect_to_email(imap_server, email_address, password):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        return mail
    except Exception as e:
        raise ConnectionError(f"Failed to connect to the email server: {e}")

def fetch_unread_emails(mail):
    try:
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            raise ValueError("Failed to fetch unread emails.")
        email_ids = messages[0].split()
        return email_ids
    except Exception as e:
        raise RuntimeError(f"Error fetching unread emails: {e}")

def parse_email(mail, email_id):
    try:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        if status != "OK":
            raise ValueError("Failed to fetch email content.")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                return subject, body
        return None, None
    except Exception as e:
        raise RuntimeError(f"Error parsing email: {e}")

def classify_email(api_key, subject, body):
    try:
        openai.api_key = api_key
        chat = ChatCompletion()
        prompt = f"Classify the following email into categories (e.g., 'work', 'personal', 'urgent').\nSubject: {subject}\nBody: {body}\n"
        response = chat.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        raise RuntimeError(f"Error classifying email: {e}")

def process_emails(imap_server, email_address, password, api_key):
    try:
        mail = connect_to_email(imap_server, email_address, password)
        email_ids = fetch_unread_emails(mail)
        processed_emails = []

        for email_id in email_ids:
            subject, body = parse_email(mail, email_id)
            if subject and body:
                category = classify_email(api_key, subject, body)
                processed_emails.append({"subject": subject, "category": category})

        mail.logout()
        return processed_emails
    except Exception as e:
        raise RuntimeError(f"Error processing emails: {e}")

def main():
    parser = argparse.ArgumentParser(description="Email AI Sorter")
    parser.add_argument("--imap-server", required=True, help="IMAP server address")
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--password", required=True, help="Email password")
    parser.add_argument("--api-key", required=True, help="Claude AI API key")
    args = parser.parse_args()

    try:
        processed_emails = process_emails(args.imap_server, args.email, args.password, args.api_key)
        print("Processed Emails:")
        for email_info in processed_emails:
            print(f"Subject: {email_info['subject']} | Category: {email_info['category']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()