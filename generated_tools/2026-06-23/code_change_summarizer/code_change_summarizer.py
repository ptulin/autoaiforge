import argparse
import os
from git import Repo, GitCommandError
import openai

def summarize_diff(diff_text, model="gpt-3.5-turbo"):
    """Summarize the given diff text using OpenAI's API."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes code changes."},
                {"role": "user", "content": f"Summarize the following code diff:\n{diff_text}"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating summary: {e}"

def get_commit_diffs(repo_path, commit_range):
    """Retrieve diffs for the specified commit range in the repository."""
    try:
        repo = Repo(repo_path)
        if ".." in commit_range:
            commits = repo.git.log("--pretty=format:%H", commit_range).splitlines()
        else:
            commits = [commit_range]
        
        diffs = []
        for commit_hash in commits:
            commit = repo.commit(commit_hash)
            diffs.append(commit.diff(create_patch=True))
        return diffs
    except GitCommandError as e:
        raise ValueError(f"Error accessing git repository or commit range: {e}")

def generate_summaries(repo_path, commit_range, output_format):
    """Generate summaries for code changes in the specified commit range."""
    diffs = get_commit_diffs(repo_path, commit_range)
    summaries = []

    for diff in diffs:
        for diff_item in diff:
            diff_text = diff_item.diff.decode('utf-8', errors='ignore')
            summary = summarize_diff(diff_text)
            summaries.append({
                "file": diff_item.b_path,
                "summary": summary
            })

    if output_format == "markdown":
        return generate_markdown_report(summaries)
    else:
        return generate_text_report(summaries)

def generate_markdown_report(summaries):
    """Generate a Markdown report from summaries."""
    report = "# Code Change Summary\n\n"
    for summary in summaries:
        report += f"## File: {summary['file']}\n\n{summary['summary']}\n\n"
    return report

def generate_text_report(summaries):
    """Generate a plain text report from summaries."""
    report = "Code Change Summary\n\n"
    for summary in summaries:
        report += f"File: {summary['file']}\n{summary['summary']}\n\n"
    return report

def main():
    parser = argparse.ArgumentParser(description="Code Change Summarizer")
    parser.add_argument("--repo", required=True, help="Path to the local Git repository")
    parser.add_argument("--range", required=True, help="Commit range (e.g., HEAD~5..HEAD)")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--format", choices=["text", "markdown"], default="text", help="Output format")

    args = parser.parse_args()

    if not os.path.exists(args.repo):
        print(f"Error: Repository path '{args.repo}' does not exist.")
        return

    try:
        summaries = generate_summaries(args.repo, args.range, args.format)
        with open(args.output, "w") as f:
            f.write(summaries)
        print(f"Summary written to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()