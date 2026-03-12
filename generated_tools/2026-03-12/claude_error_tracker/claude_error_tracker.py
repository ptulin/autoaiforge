import logging
import traceback
from openai import ChatCompletion

class ClaudeTracker:
    def __init__(self, api_key):
        """
        Initialize the ClaudeTracker with the provided API key.

        :param api_key: API key for accessing Claude AI (via OpenAI API)
        """
        self.api_key = api_key
        self.logger = logging.getLogger("ClaudeTracker")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def start(self):
        """
        Start the error tracking by setting up a global exception hook.
        """
        self.logger.info("ClaudeTracker started. Capturing uncaught exceptions.")
        import sys
        sys.excepthook = self._handle_exception

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Handle uncaught exceptions, log them, and send them to Claude for analysis.

        :param exc_type: Exception type
        :param exc_value: Exception value
        :param exc_traceback: Exception traceback
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow keyboard interrupts to pass through
            import sys
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error("Unhandled exception captured:\n%s", error_message)

        try:
            suggestions = self._analyze_error_with_claude(error_message)
            self.logger.info("Claude's suggestions:\n%s", suggestions)
        except Exception as e:
            self.logger.error("Failed to analyze error with Claude: %s", str(e))

    def _analyze_error_with_claude(self, error_message):
        """
        Send the error message to Claude AI for analysis and return suggestions.

        :param error_message: The error message to analyze
        :return: Suggestions from Claude AI
        """
        ChatCompletion.api_key = self.api_key
        try:
            response = ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that helps debug Python errors."},
                    {"role": "user", "content": f"Here is a Python error:\n{error_message}\nCan you provide suggestions to fix it?"}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise RuntimeError(f"Error communicating with Claude API: {str(e)}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the Claude Error Tracker.")
    parser.add_argument("--api_key", required=True, help="API key for Claude AI integration.")
    args = parser.parse_args()

    tracker = ClaudeTracker(api_key=args.api_key)
    tracker.start()

    # Simulate an error for demonstration purposes
    raise ValueError("This is a test error.")