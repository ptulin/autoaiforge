import os
import difflib
import argparse
import requests

def fetch_public_repositories():
    """Fetch a list of public repositories containing source code snippets."""
    try:
        response = requests.get("https://api.github.com/repositories")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return []

def read_source_code(file_path):
    """Read the source code from the given file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def compare_code_with_repositories(source_code, repositories):
    """Compare the source code with repositories using fuzzy matching."""
    matches = []
    for repo in repositories:
        repo_name = repo.get("full_name", "Unknown Repository")
        repo_url = repo.get("html_url", "Unknown URL")

        # Simulate fetching code snippets from the repository
        repo_code_snippets = repo.get("code_snippets", [])

        for snippet in repo_code_snippets:
            similarity = difflib.SequenceMatcher(None, source_code, snippet).ratio()
            if similarity > 0.8:  # Threshold for similarity
                matches.append({
                    "repository": repo_name,
                    "url": repo_url,
                    "snippet": snippet,
                    "similarity": similarity
                })
    return matches

def generate_compliance_report(matches):
    """Generate a compliance report based on the matches."""
    report_lines = ["Compliance Report:"]
    if not matches:
        report_lines.append("No potential copyright issues detected.")
    else:
        for match in matches:
            report_lines.append(f"Repository: {match['repository']}")
            report_lines.append(f"URL: {match['url']}")
            report_lines.append(f"Snippet: {match['snippet']}")
            report_lines.append(f"Similarity: {match['similarity']:.2f}")
            report_lines.append("---")
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description="Source Code Provenance Checker")
    parser.add_argument("--path", required=True, help="Path to the source code file or directory")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist.")
        return

    if os.path.isdir(args.path):
        print("Error: Only single file input is supported currently.")
        return

    source_code = read_source_code(args.path)
    if not source_code:
        print("Error: Could not read source code.")
        return

    repositories = fetch_public_repositories()
    if not repositories:
        print("Error: Could not fetch public repositories.")
        return

    matches = compare_code_with_repositories(source_code, repositories)
    report = generate_compliance_report(matches)
    print(report)

if __name__ == "__main__":
    main()
