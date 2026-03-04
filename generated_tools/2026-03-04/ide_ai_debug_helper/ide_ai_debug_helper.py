import traceback
import sys
from openai import ChatCompletion
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import threading

class IDEAIDebugHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.lock = threading.Lock()

    def analyze_exception(self, exc_type, exc_value, exc_traceback):
        """Analyzes the exception and provides suggestions."""
        formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print("\nException occurred:\n")
        print(highlight(formatted_traceback, PythonLexer(), TerminalFormatter()))

        with self.lock:
            try:
                print("Analyzing exception with Claude AI...\n")
                response = self._query_claude_ai(formatted_traceback)
                print("Claude AI Suggestions:\n")
                print(highlight(response, PythonLexer(), TerminalFormatter()))
            except Exception as e:
                print("Error while querying Claude AI:", e)

    def _query_claude_ai(self, traceback_text):
        """Send the traceback to Claude AI and get suggestions."""
        ChatCompletion.api_key = self.api_key
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI debugging assistant."},
                {"role": "user", "content": f"Analyze this Python exception and provide suggestions:\n{traceback_text}"}
            ]
        )
        return response['choices'][0]['message']['content']

    def start(self):
        """Start the IDE AI Debug Helper."""
        sys.excepthook = self.analyze_exception

# Singleton instance
_debug_helper_instance = None

def start(api_key):
    """Start the IDE AI Debug Helper with the provided API key."""
    global _debug_helper_instance
    if _debug_helper_instance is None:
        _debug_helper_instance = IDEAIDebugHelper(api_key)
    _debug_helper_instance.start()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IDE AI Debug Helper")
    parser.add_argument("--api-key", required=True, help="Your OpenAI API key")
    args = parser.parse_args()

    start(args.api_key)
