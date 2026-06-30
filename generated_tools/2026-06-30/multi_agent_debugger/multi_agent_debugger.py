import argparse
import logging
import json
from rich.console import Console
from rich.table import Table
from rich.live import Live
from time import time

# Initialize the logger
logger = logging.getLogger("multi_agent_debugger")

class MultiAgentDebugger:
    def __init__(self, input_source, level):
        self.input_source = input_source
        self.level = level
        self.console = Console()
        self.start_time = time()

    def setup_logging(self):
        log_level = logging.DEBUG if self.level == "verbose" else logging.INFO
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    def parse_input(self):
        """Parse input source, which can be a log file or live feed."""
        try:
            with open(self.input_source, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_source}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from: {self.input_source}")
            return []

    def display_logs(self, events):
        """Display logs in a formatted table."""
        table = Table(title="Multi-Agent Debugger Logs")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Agent", style="green")
        table.add_column("Event", style="magenta")
        table.add_column("Details", style="yellow")

        for event in events:
            timestamp = event.get("timestamp", "N/A")
            agent = event.get("agent", "N/A")
            event_type = event.get("event", "N/A")
            details = event.get("details", "N/A")
            table.add_row(str(timestamp), agent, event_type, details)

        with Live(table, refresh_per_second=4, console=self.console):
            pass

    def run(self):
        """Main execution method."""
        self.setup_logging()
        logger.info("Starting Multi-Agent Debugger")

        events = self.parse_input()
        if not events:
            logger.warning("No events to display. Exiting.")
            return

        self.display_logs(events)
        logger.info("Finished displaying logs.")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Debugger")
    parser.add_argument("--input", required=True, help="Path to the input log file (JSON format)")
    parser.add_argument("--level", choices=["info", "verbose"], default="info", help="Debugging level")

    args = parser.parse_args()

    debugger = MultiAgentDebugger(input_source=args.input, level=args.level)
    debugger.run()

if __name__ == "__main__":
    main()