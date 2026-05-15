import argparse
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_usage(api_key):
    """Fetch usage data from the Claude API."""
    url = "https://api.claude.ai/usage"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching usage data: {e}")
        return None

def monitor_usage(api_key, alert_threshold, max_iterations=5):
    """Monitor API usage in real-time and send alerts if threshold is exceeded."""
    print("Starting real-time monitoring...")
    iterations = 0
    while iterations < max_iterations:
        usage_data = fetch_usage(api_key)
        if usage_data:
            requests_per_minute = usage_data.get("requests_per_minute", 0)
            usage_limit = usage_data.get("usage_limit", 100)
            usage_percentage = (requests_per_minute / usage_limit) * 100

            print(f"Requests per minute: {requests_per_minute}, Usage: {usage_percentage:.2f}%")

            if usage_percentage >= alert_threshold:
                print(f"ALERT: Usage exceeded {alert_threshold}% of the limit!")
        time.sleep(1)  # Reduced sleep time for testing purposes
        iterations += 1

def generate_report(api_key, time_range, output_file):
    """Generate a usage report over a specified time range."""
    print(f"Generating report for the last {time_range} minutes...")
    end_time = datetime.now()
    start_time = end_time - pd.Timedelta(minutes=time_range)

    timestamps = []
    usage_percentages = []

    for _ in range(time_range):
        usage_data = fetch_usage(api_key)
        if usage_data:
            requests_per_minute = usage_data.get("requests_per_minute", 0)
            usage_limit = usage_data.get("usage_limit", 100)
            usage_percentage = (requests_per_minute / usage_limit) * 100

            timestamps.append(datetime.now())
            usage_percentages.append(usage_percentage)
        time.sleep(1)  # Reduced sleep time for testing purposes

    df = pd.DataFrame({"Timestamp": timestamps, "Usage Percentage": usage_percentages})
    df.to_csv(output_file, index=False)
    print(f"Report saved to {output_file}")

    plt.plot(df["Timestamp"], df["Usage Percentage"], label="Usage Percentage")
    plt.xlabel("Timestamp")
    plt.ylabel("Usage Percentage")
    plt.title("Claude API Usage Report")
    plt.legend()
    plt.savefig(output_file.replace(".csv", ".png"))
    print(f"Graph saved to {output_file.replace('.csv', '.png')}")

def main():
    parser = argparse.ArgumentParser(description="Claude Usage Monitor")
    parser.add_argument("--api-key", required=True, help="API key for Claude AI")
    parser.add_argument("--alert-threshold", type=int, default=80, help="Alert threshold percentage")
    parser.add_argument("--generate-report", action="store_true", help="Generate usage report")
    parser.add_argument("--time-range", type=int, default=60, help="Time range for report in minutes")
    parser.add_argument("--output-file", default="usage_report.csv", help="Output file for the report")

    args = parser.parse_args()

    if args.generate_report:
        generate_report(args.api_key, args.time_range, args.output_file)
    else:
        monitor_usage(args.api_key, args.alert_threshold)

if __name__ == "__main__":
    main()
