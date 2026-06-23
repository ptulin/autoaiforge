import argparse
import json
from datetime import datetime
from collections import Counter
import os

import matplotlib.pyplot as plt
import numpy as np
from git import Repo

def analyze_repository(repo_path):
    """
    Analyze the commit history of a Git repository.

    Args:
        repo_path (str): Path to the local Git repository.

    Returns:
        dict: A dictionary containing commit analysis data.
    """
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repository path '{repo_path}' does not exist.")

    try:
        repo = Repo(repo_path)
    except Exception as e:
        raise ValueError(f"Error opening repository: {e}")

    if repo.bare:
        raise ValueError("The repository is bare and has no commit history.")

    commits = list(repo.iter_commits())
    if not commits:
        return {
            "commit_frequency": {
                "dates": [],
                "counts": []
            },
            "contributor_activity": {}
        }

    commit_dates = [datetime.fromtimestamp(commit.committed_date).date() for commit in commits]
    commit_authors = [commit.author.name for commit in commits]

    # Analyze commit frequency over time
    date_counts = Counter(commit_dates)
    sorted_dates = sorted(date_counts.items())
    dates, counts = zip(*sorted_dates) if sorted_dates else ([], [])

    # Analyze contributor activity
    author_counts = Counter(commit_authors)

    return {
        "commit_frequency": {
            "dates": [date.isoformat() for date in dates],
            "counts": list(counts)
        },
        "contributor_activity": dict(author_counts)
    }

def generate_visualizations(analysis, output_dir):
    """
    Generate visualizations from the analysis data.

    Args:
        analysis (dict): The analysis data.
        output_dir (str): Directory to save the visualizations.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Commit frequency over time
    dates = [datetime.fromisoformat(date) for date in analysis["commit_frequency"]["dates"]]
    counts = analysis["commit_frequency"]["counts"]

    if dates and counts:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, counts, marker="o")
        plt.title("Commit Frequency Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Commits")
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "commit_frequency.png"))
        plt.close()

    # Contributor activity
    authors = list(analysis["contributor_activity"].keys())
    contributions = list(analysis["contributor_activity"].values())

    if authors and contributions:
        y_pos = np.arange(len(authors))

        plt.figure(figsize=(10, 6))
        plt.barh(y_pos, contributions, align="center")
        plt.yticks(y_pos, authors)
        plt.xlabel("Number of Commits")
        plt.title("Contributor Activity")
        plt.savefig(os.path.join(output_dir, "contributor_activity.png"))
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="Repository Commit Analyzer")
    parser.add_argument("--repo", required=True, help="Path to the local Git repository.")
    parser.add_argument("--output", required=True, help="Path to save the output JSON file.")
    parser.add_argument("--visualizations", default="visualizations", help="Directory to save visualizations.")

    args = parser.parse_args()

    try:
        analysis = analyze_repository(args.repo)

        # Save analysis to JSON file
        with open(args.output, "w") as json_file:
            json.dump(analysis, json_file, indent=4)

        # Generate visualizations
        generate_visualizations(analysis, args.visualizations)

        print(f"Analysis complete. Results saved to {args.output} and visualizations saved to {args.visualizations}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
