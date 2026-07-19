import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SecurePromptSanitizer")

def sanitize_prompt(prompt: str, custom_filters: list = None) -> str:
    """
    Sanitizes a given prompt by applying default and custom filters.

    Args:
        prompt (str): The raw input prompt to sanitize.
        custom_filters (list): Optional list of custom regex patterns to apply.

    Returns:
        str: The sanitized prompt.
    """
    if not isinstance(prompt, str):
        raise ValueError("Input prompt must be a string.")

    if not prompt.strip():
        logger.info("Received an empty or whitespace-only prompt.")
        return ""

    # Default filters to sanitize common problematic patterns
    default_filters = [
        r"(?i)delete\s+all\s+files",  # Prevent destructive instructions
        r"(?i)shutdown\s+system",      # Prevent system shutdown commands
        r"(?i)format\s+drive",        # Prevent drive formatting commands
        r"(?i)password\s*:.*",        # Remove password disclosures
        r"(?i)api\s+key\s*:.*"       # Remove API key disclosures
    ]

    # Combine default filters with custom filters if provided
    filters = default_filters + (custom_filters or [])

    sanitized_prompt = prompt
    for pattern in filters:
        sanitized_prompt = re.sub(pattern, "[REDACTED]", sanitized_prompt)

    if sanitized_prompt != prompt:
        logger.info("Prompt sanitized. Original: %s | Sanitized: %s", prompt, sanitized_prompt)
    else:
        logger.info("No sanitization needed for the prompt.")

    return sanitized_prompt

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Secure Prompt Sanitizer")
    parser.add_argument("prompt", type=str, help="The raw prompt to sanitize.")
    parser.add_argument("--custom-filters", nargs="*", help="Optional custom regex filters to apply.", default=[])

    args = parser.parse_args()

    sanitized = sanitize_prompt(args.prompt, args.custom_filters)
    print(sanitized)
