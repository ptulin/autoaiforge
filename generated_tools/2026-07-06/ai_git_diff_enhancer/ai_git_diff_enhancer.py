import argparse
import os
import git
import openai
import sys

def generate_ai_explanation(diff_text):
    """
    Generate AI-based explanations for the given diff text using OpenAI API.

    Args:
        diff_text (str): The Git diff text.

    Returns:
        str: AI-generated explanation.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Explain the following code diff and suggest improvements:\n{diff_text}",
            max_tokens=300
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating AI explanation: {e}"

def get_git_diff(commit_hash=None, branch_name=None, diff_file=None):
    """
    Retrieve the Git diff based on the input parameters.

    Args:
        commit_hash (str): The commit hash to get the diff for.
        branch_name (str): The branch name to compare with HEAD.
        diff_file (str): Path to a diff file.

    Returns:
        str: The Git diff text.
    """
    try:
        if diff_file:
            if not os.path.exists(diff_file):
                raise FileNotFoundError(f"Diff file '{diff_file}' not found.")
            with open(diff_file, 'r') as file:
                return file.read()

        repo = git.Repo('.')

        if commit_hash:
            commit = repo.commit(commit_hash)
            return repo.git.diff(commit.parents[0], commit) if commit.parents else repo.git.show(commit_hash)

        if branch_name:
            return repo.git.diff(branch_name)

        raise ValueError("You must provide either a commit hash, branch name, or diff file.")

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        return f"Error retrieving Git diff: {e}"

def main():
    parser = argparse.ArgumentParser(description="AI Git Diff Enhancer")
    parser.add_argument('--commit', type=str, default=None, help='Git commit hash to analyze.')
    parser.add_argument('--branch', type=str, default=None, help='Git branch name to compare with HEAD.')
    parser.add_argument('--diff-file', type=str, default=None, help='Path to a diff file.')
    parser.add_argument('--output', type=str, default=None, help='Path to save the annotated diff as a markdown file.')
    args = parser.parse_args()

    diff_text = get_git_diff(commit_hash=args.commit, branch_name=args.branch, diff_file=args.diff_file)

    if diff_text.startswith("Error"):
        print(diff_text)
        sys.exit(1)

    explanation = generate_ai_explanation(diff_text)

    annotated_diff = f"### Original Diff:\n\n{diff_text}\n\n### AI Explanation:\n\n{explanation}"

    if args.output:
        try:
            with open(args.output, 'w') as file:
                file.write(annotated_diff)
            print(f"Annotated diff saved to {args.output}")
        except Exception as e:
            print(f"Error saving annotated diff: {e}")
            sys.exit(1)
    else:
        print(annotated_diff)

if __name__ == '__main__':
    main()
