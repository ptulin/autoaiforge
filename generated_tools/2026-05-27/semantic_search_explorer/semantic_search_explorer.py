import argparse
import requests
from rich.console import Console
from rich.table import Table

def perform_search(query, api_key, api_url):
    """
    Perform a semantic search using the provided API.

    Args:
        query (str): The search query.
        api_key (str): The API key for authentication.
        api_url (str): The API endpoint URL.

    Returns:
        list: A list of search results with metadata.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"query": query}

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to perform search: {e}")

def display_results(results):
    """
    Display search results in a formatted table.

    Args:
        results (list): A list of search results with metadata.
    """
    console = Console()
    table = Table(title="Semantic Search Results")

    table.add_column("Rank", style="cyan", justify="center")
    table.add_column("Title", style="green")
    table.add_column("Source", style="magenta")
    table.add_column("Relevance Score", style="yellow", justify="center")

    for idx, result in enumerate(results, start=1):
        table.add_row(
            str(idx),
            result.get("title", "N/A"),
            result.get("source", "N/A"),
            str(result.get("relevance_score", "N/A"))
        )

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Semantic Search Explorer")
    parser.add_argument("--query", required=True, help="Search query to execute")
    parser.add_argument("--api_key", required=True, help="API key for authentication")
    parser.add_argument("--api_url", default="https://api.example.com/search", help="API endpoint URL")

    args = parser.parse_args()

    try:
        results = perform_search(args.query, args.api_key, args.api_url)
        if results:
            display_results(results)
        else:
            print("No results found.")
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()