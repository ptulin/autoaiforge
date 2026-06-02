import argparse
import openai
import os

def llm_code_assistant(query=None, file=None, output=None):
    """
    LLM Code Assistant: Generate code snippets, provide debugging suggestions, or refactor code.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        return "Error: OPENAI_API_KEY environment variable not set."

    if not query and not file:
        return "Error: Either --query or --file must be provided."

    try:
        if query:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{query}",
                max_tokens=150
            )
            result = response.choices[0].text.strip()

            if output:
                with open(output, 'w') as f:
                    f.write(result)

            return result

        elif file:
            if not os.path.exists(file):
                return "Error: File not found."

            with open(file, 'r') as f:
                code_content = f.read()

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Refactor and optimize the following Python code:\n{code_content}",
                max_tokens=300
            )
            result = response.choices[0].text.strip()

            if output:
                with open(output, 'w') as f:
                    f.write(result)

            return result

    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI API: {e}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LLM Code Assistant: Generate code snippets, provide debugging suggestions, or refactor code.")
    parser.add_argument('--query', type=str, help='Natural language query for code generation or debugging.')
    parser.add_argument('--file', type=str, help='Path to a code file for refactoring or optimization.')
    parser.add_argument('--output', type=str, help='Path to save the generated or refactored code.')

    args = parser.parse_args()

    result = llm_code_assistant(query=args.query, file=args.file, output=args.output)
    if result:
        print(result)