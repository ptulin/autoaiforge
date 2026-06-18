import argparse
from rich.console import Console
from rich.text import Text
import tiktoken

def simulate_context_window(prompt: str, window_size: int) -> Text:
    """
    Simulates the truncation of a language model's context window.

    Args:
        prompt (str): The input prompt text.
        window_size (int): The maximum number of tokens allowed in the context window.

    Returns:
        Text: A visualization of retained and truncated tokens.
    """
    # Initialize tokenizer
    try:
        tokenizer = tiktoken.get_encoding("gpt2")
    except Exception as e:
        raise RuntimeError("Failed to initialize tokenizer. Ensure tiktoken is installed.") from e

    tokens = tokenizer.encode(prompt)
    retained_tokens = tokens[:window_size]
    truncated_tokens = tokens[window_size:]

    retained_text = tokenizer.decode(retained_tokens)
    truncated_text = tokenizer.decode(truncated_tokens)

    # Create visualization using rich
    text = Text()

    text.append(retained_text, style="bold green")
    if truncated_text:
        text.append(" [TRUNCATED] ", style="bold red")
        text.append(truncated_text, style="red")

    return text

def main():
    parser = argparse.ArgumentParser(
        description="Context Window Simulator: Simulates a language model's context window to visualize token truncation."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the input text file containing the prompt."
    )
    parser.add_argument(
        "--window", type=int, required=True, help="The context window size (e.g., 4096 for GPT-4)."
    )

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as file:
            prompt = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
        return
    except Exception as e:
        print(f"Error: Unable to read the file. {e}")
        return

    if not prompt.strip():
        print("Error: The input file is empty.")
        return

    try:
        visualization = simulate_context_window(prompt, args.window)
        console = Console()
        console.print(visualization)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
