import argparse
import json
import os
import smtplib
from email.mime.text import MIMEText
from plyer import notification
import requests
import schedule
import time

def fetch_news(keywords, sources):
    """Fetch news articles from the given sources and filter by keywords."""
    filtered_articles = []
    for source in sources:
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            for article in articles:
                if any(keyword.lower() in article.get('title', '').lower() for keyword in keywords):
                    filtered_articles.append(article)
        except (requests.RequestException, json.JSONDecodeError):
            print(f"Error fetching or parsing news from {source}")
    return filtered_articles

def send_email_notification(email_config, articles):
    """Send email notifications for the filtered articles."""
    try:
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            for article in articles:
                msg = MIMEText(f"{article['title']}\n{article['url']}")
                msg['Subject'] = 'AI News Alert'
                msg['From'] = email_config['username']
                msg['To'] = email_config['to']
                server.sendmail(email_config['username'], email_config['to'], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

def send_desktop_notification(articles):
    """Send desktop notifications for the filtered articles."""
    for article in articles:
        notification.notify(
            title='AI News Alert',
            message=f"{article['title']}",
            app_name='AI News Notifier'
        )

def monitor_news(keywords, sources, notify_method, email_config=None):
    """Monitor news and send notifications based on the configured method."""
    articles = fetch_news(keywords, sources)
    if articles:
        if notify_method == 'email' and email_config:
            send_email_notification(email_config, articles)
        elif notify_method == 'desktop':
            send_desktop_notification(articles)
        else:
            print("Invalid notification method or missing configuration.")

def load_config(config_file):
    """Load configuration from a JSON file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    with open(config_file, 'r') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description='AI News Notifier')
    parser.add_argument('--config', required=True, help='Path to configuration JSON file')
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        keywords = config.get('keywords', [])
        sources = config.get('sources', [])
        notify_method = config.get('notify_method', 'desktop')
        email_config = config.get('email_config', None)

        if not keywords or not sources:
            print("Keywords and sources must be specified in the configuration.")
            return

        schedule.every(config.get('frequency', 10)).minutes.do(
            monitor_news, keywords, sources, notify_method, email_config
        )

        print("AI News Notifier is running. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()