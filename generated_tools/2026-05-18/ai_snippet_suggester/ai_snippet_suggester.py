import argparse
import openai
import os

def generate_snippet(description, language, temperature=0.7, max_tokens=150):
    """
    Generate a code snippet based on the given description and language.

    Args:
        description (str): Problem description or function idea.
        language (str): Programming language for the snippet.
        temperature (float): Sampling temperature for the model.
        max_tokens (int): Maximum tokens for the response.

    Returns:
        str: Generated code snippet.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Write a {language} code snippet for the following problem: {description}",
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error generating snippet: {str(e)}"
    except Exception as e:
        return f"Error generating snippet: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="AI Snippet Suggester: Generate code snippets using OpenAI API.")
    parser.add_argument("--description", required=True, help="Problem description or function idea.")
    parser.add_argument("--language", required=True, help="Programming language for the snippet.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature for the model (default: 0.7).")
    parser.add_argument("--max_tokens", type=int, default=150, help="Maximum tokens for the response (default: 150).")
    parser.add_argument("--output", help="File path to save the generated snippet.")

    args = parser.parse_args()

    # Generate the code snippet
    snippet = generate_snippet(args.description, args.language, args.temperature, args.max_tokens)

    if args.output:
        try:
            with open(args.output, "w") as file:
                file.write(snippet)
            print(f"Snippet saved to {args.output}")
        except IOError as e:
            print(f"Error saving snippet to file: {str(e)}")
    else:
        print("Generated Snippet:")
        print(snippet)

if __name__ == "__main__":
    main()