import argparse
import json
import openai

def optimize_query(query, api_key):
    """Optimize a search query using OpenAI's API."""
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Optimize the following search query for better results: {query}",
            max_tokens=100
        )
        optimized_query = response.choices[0].text.strip()
        return optimized_query
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to optimize query: {e}")

def save_output(output, file_path, output_format):
    """Save the optimized query to a file in the specified format."""
    if output_format == "json":
        with open(file_path, "w") as f:
            json.dump({"optimized_query": output}, f, indent=4)
    elif output_format == "text":
        with open(file_path, "w") as f:
            f.write(output)
    else:
        raise ValueError("Unsupported output format. Use 'json' or 'text'.")

def main():
    parser = argparse.ArgumentParser(description="AI Query Optimizer")
    parser.add_argument("--query", type=str, help="Search query to optimize.")
    parser.add_argument("--input_file", type=str, help="Path to a text file containing the search query.")
    parser.add_argument("--output", type=str, help="File path to save the optimized query.")
    parser.add_argument("--format", type=str, choices=["json", "text"], default="json", help="Output format (default: json).")
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key.")

    args = parser.parse_args()

    if not args.query and not args.input_file:
        parser.error("Either --query or --input_file must be provided.")

    if args.query:
        query = args.query
    else:
        try:
            with open(args.input_file, "r") as f:
                query = f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{args.input_file}' not found.")

    try:
        optimized_query = optimize_query(query, args.api_key)
        print("Optimized Query:", optimized_query)

        if args.output:
            save_output(optimized_query, args.output, args.format)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()