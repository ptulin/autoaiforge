import re
import logging
from inspect import signature

class PrivacyGuard:
    def __init__(self, rules=None):
        """
        Initialize the PrivacyGuard with a set of rules.

        :param rules: List of regex patterns to identify sensitive data.
        """
        self.rules = rules or []
        self.logger = logging.getLogger('PrivacyGuard')
        logging.basicConfig(level=logging.INFO)

    def add_rule(self, rule):
        """
        Add a new regex rule for detecting sensitive data.

        :param rule: A regex pattern as a string.
        """
        self.rules.append(rule)

    def check(self, text):
        """
        Analyze the given text for sensitive data based on the rules.

        :param text: The text to analyze.
        :return: The sanitized text if no sensitive data is detected.
        :raises ValueError: If sensitive data is detected.
        """
        for rule in self.rules:
            if re.search(rule, text):
                self.logger.warning(f"Sensitive data detected: {rule}")
                raise ValueError("Sensitive data detected based on privacy rules.")
        return text

    def wrap(self, func):
        """
        Wrap a function to intercept its text input and check for sensitive data.

        :param func: The function to wrap.
        :return: A wrapped function.
        """
        def wrapped(*args, **kwargs):
            sig = signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for name, value in bound_args.arguments.items():
                if isinstance(value, str):
                    self.check(value)

            return func(*args, **kwargs)

        return wrapped

if __name__ == "__main__":
    # Example usage
    guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])

    try:
        print(guard.check("This is a test with password."))
    except ValueError as e:
        print(e)

    @guard.wrap
    def example_function(input_text):
        return f"Processed: {input_text}"

    try:
        print(example_function("This contains secret information."))
    except ValueError as e:
        print(e)