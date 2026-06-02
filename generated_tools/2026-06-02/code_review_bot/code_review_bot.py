import argparse
import os
import openai
import flake8.api.legacy as flake8
from typing import List

def analyze_code_with_flake8(file_path: str) -> List[str]:
    """Analyze a Python file using flake8 and return a list of issues."""
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files([file_path])
    issues = []
    for line in report._deferred_print:
        issues.append(line)
    return issues

def analyze_code_with_openai(file_content: str) -> str:
    """Analyze Python code using OpenAI's API and return feedback."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Review the following Python code and provide feedback on potential issues, improvements, and best practices compliance:\n\n{file_content}\n\nFeedback:",
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error during OpenAI API call: {e}"

def process_file(file_path: str, save_output: bool = False) -> str:
    """Process a single Python file for code review."""
    if not os.path.isfile(file_path):
        return f"Error: File '{file_path}' does not exist."

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"

    flake8_issues = analyze_code_with_flake8(file_path)
    openai_feedback = analyze_code_with_openai(file_content)

    report = f"Code Review Report for {file_path}\n\n"
    report += "Flake8 Issues:\n" + ("\n".join(flake8_issues) if flake8_issues else "No issues found.") + "\n\n"
    report += "OpenAI Feedback:\n" + openai_feedback + "\n"

    if save_output:
        output_file = f"{file_path}_review.txt"
        try:
            with open(output_file, 'w') as file:
                file.write(report)
            report += f"\nReport saved to {output_file}"
        except Exception as e:
            report += f"\nError saving report: {e}"

    return report

def process_directory(directory_path: str, save_output: bool = False) -> str:
    """Process all Python files in a directory for code review."""
    if not os.path.isdir(directory_path):
        return f"Error: Directory '{directory_path}' does not exist."

    reports = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                reports.append(process_file(file_path, save_output))

    return "\n\n".join(reports)

def main():
    parser = argparse.ArgumentParser(description="Code Review Bot: Automated Python code reviews with AI feedback.")
    parser.add_argument('--path', required=True, help="Path to a Python file or directory.")
    parser.add_argument('--save', action='store_true', help="Save the review report to a file.")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        result = process_file(args.path, args.save)
    elif os.path.isdir(args.path):
        result = process_directory(args.path, args.save)
    else:
        result = f"Error: Path '{args.path}' is neither a file nor a directory."

    print(result)

if __name__ == "__main__":
    main()
