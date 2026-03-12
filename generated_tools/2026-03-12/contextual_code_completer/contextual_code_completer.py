import os
import openai
import argparse

def analyze_codebase(directory):
    """
    Analyzes the codebase in the given directory and extracts context.

    Args:
        directory (str): Path to the project directory.

    Returns:
        str: A string representation of the codebase context.
    """
    context = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        context.append(code)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    return '\n'.join(context)

def generate_code(context, query):
    """
    Generates code based on the provided context and query using OpenAI's API.

    Args:
        context (str): The codebase context.
        query (str): The query string describing the desired operation.

    Returns:
        str: The generated code snippet.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Context:\n{context}\n\nQuery: {query}\n\nGenerated Code:",
            max_tokens=150,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Error generating code: {e}")

def main():
    """
    Main function to analyze the codebase and generate code based on the query.

    Args:
        None
    """
    parser = argparse.ArgumentParser(description="Context-aware code generator.")
    parser.add_argument('--path', required=True, type=str, help='Path to the project directory.')
    parser.add_argument('--query', required=True, type=str, help='Query string for the desired code operation.')
    args = parser.parse_args()

    try:
        print("Analyzing codebase...")
        context = analyze_codebase(args.path)
        if not context:
            print("No Python files found in the specified directory.")
            return

        print("Generating code...")
        generated_code = generate_code(context, args.query)
        print("Generated Code:")
        print(generated_code)
    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()