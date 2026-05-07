import argparse
import sys
import openai

def analyze_email_content(email_content, mode):
    """
    Analyze email content using OpenAI's API to generate a response, summary, or action items.

    Args:
        email_content (str): The content of the email to analyze.
        mode (str): The mode of analysis ('response', 'summary', or 'action_items').

    Returns:
        str: The generated output based on the selected mode.
    """
    if not email_content.strip():
        raise ValueError("Email content is empty.")

    prompt = ""
    if mode == "response":
        prompt = f"Draft a professional response to the following email:\n{email_content}"
    elif mode == "summary":
        prompt = f"Summarize the following email thread:\n{email_content}"
    elif mode == "action_items":
        prompt = f"Extract action items or to-do lists from the following email:\n{email_content}"
    else:
        raise ValueError("Invalid mode. Choose from 'response', 'summary', or 'action_items'.")

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Claude Email Automation: Analyze email content and generate intelligent responses, summaries, or action items."
    )
    parser.add_argument(
        "--email-file", type=str, help="Path to the email content file.", required=False
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["response", "summary", "action_items"],
        required=True,
        help="Mode of operation: 'response', 'summary', or 'action_items'.",
    )

    args = parser.parse_args()

    if args.email_file:
        try:
            with open(args.email_file, "r", encoding="utf-8") as file:
                email_content = file.read()
        except FileNotFoundError:
            print(f"Error: File '{args.email_file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Reading email content from stdin. Press Ctrl+D (or Ctrl+Z on Windows) to end input.")
        email_content = sys.stdin.read()

    try:
        result = analyze_email_content(email_content, args.mode)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()