import argparse
import os
import openai
import git
import yaml
from git import Repo

def analyze_git_diff(repo_path, branch=None, commit_hash=None):
    try:
        repo = Repo(repo_path)
        if branch:
            repo.git.checkout(branch)
        elif commit_hash:
            repo.git.checkout(commit_hash)
        
        diff = repo.git.diff('HEAD~1', 'HEAD')
        return diff
    except Exception as e:
        raise RuntimeError(f"Error analyzing git diff: {e}")

def generate_docstring(diff, openai_api_key):
    try:
        openai.api_key = openai_api_key
        prompt = f"Analyze the following git diff and generate a concise explanation of the changes:\n{diff}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating docstring: {e}")

def update_documentation(repo_path, docstring):
    try:
        readme_path = os.path.join(repo_path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'a') as readme_file:
                readme_file.write(f"\n\n## Recent Changes\n{docstring}")
        else:
            raise FileNotFoundError("README.md not found in the repository.")
    except Exception as e:
        raise RuntimeError(f"Error updating documentation: {e}")

def main():
    parser = argparse.ArgumentParser(description="Code Diff Documentation Updater")
    parser.add_argument('--repo-path', required=True, help="Path to the Git repository")
    parser.add_argument('--branch', help="Branch to analyze (optional)")
    parser.add_argument('--commit-hash', help="Specific commit hash to analyze (optional)")
    parser.add_argument('--openai-api-key', required=True, help="OpenAI API key for generating docstrings")
    
    args = parser.parse_args()
    
    try:
        diff = analyze_git_diff(args.repo_path, args.branch, args.commit_hash)
        docstring = generate_docstring(diff, args.openai_api_key)
        update_documentation(args.repo_path, docstring)
        print("Documentation updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()