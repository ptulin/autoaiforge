import psutil
import matplotlib.pyplot as plt
import typer
from typing import Optional
import time
import smtplib
from email.mime.text import MIMEText

def send_email_alert(email: str, subject: str, message: str):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = 'monitor@example.com'
        msg['To'] = email

        # Replace with your SMTP server details
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_user = 'your_username'
        smtp_password = 'your_password'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail('monitor@example.com', email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def monitor_agent(agent_id: int, alert_email: Optional[str] = None, duration: int = 60):
    """
    Monitor the health and performance of an agent.

    Args:
        agent_id (int): The process ID of the agent to monitor.
        alert_email (Optional[str]): Email to send alerts to.
        duration (int): Duration in seconds to monitor the agent.
    """
    try:
        process = psutil.Process(agent_id)
    except psutil.NoSuchProcess:
        print(f"No process found with ID {agent_id}")
        return

    metrics = []
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            cpu_usage = process.cpu_percent(interval=1)
            memory_info = process.memory_info()
            metrics.append((time.time() - start_time, cpu_usage, memory_info.rss))

            if cpu_usage > 80 and alert_email:
                send_email_alert(
                    alert_email,
                    "High CPU Usage Alert",
                    f"Agent {agent_id} is using {cpu_usage}% CPU."
                )

            print(f"Time: {time.time() - start_time:.2f}s, CPU: {cpu_usage}%, Memory: {memory_info.rss / 1024 / 1024:.2f} MB")
        except psutil.NoSuchProcess:
            print(f"Process {agent_id} terminated.")
            break

    # Plot metrics
    if metrics:
        times, cpu_usages, memory_usages = zip(*metrics)
        plt.figure(figsize=(10, 5))

        plt.subplot(2, 1, 1)
        plt.plot(times, cpu_usages, label='CPU Usage (%)')
        plt.xlabel('Time (s)')
        plt.ylabel('CPU Usage (%)')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(times, [m / 1024 / 1024 for m in memory_usages], label='Memory Usage (MB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Memory Usage (MB)')
        plt.legend()

        plt.tight_layout()
        plt.savefig('agent_metrics.png')
        print("Metrics chart saved as agent_metrics.png")

app = typer.Typer()

@app.command()
def main(agent_id: int, alert_email: Optional[str] = typer.Option(None, help="Email to send alerts to."), duration: int = typer.Option(60, help="Duration in seconds to monitor the agent.")):
    """
    Agent Health Monitor

    Monitor the health and performance of deployed autonomous AI agents.

    Args:
        agent_id (int): The process ID of the agent to monitor.
        alert_email (Optional[str]): Email to send alerts to.
        duration (int): Duration in seconds to monitor the agent.
    """
    monitor_agent(agent_id, alert_email, duration)

if __name__ == "__main__":
    app()
