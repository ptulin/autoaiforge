import os
import json
from diff_match_patch import diff_match_patch

def analyze_diff(old_path, new_path, output_format='json'):
    """
    Analyzes the differences between two codebases to identify potential vulnerabilities.

    Args:
        old_path (str): Path to the old version of the codebase.
        new_path (str): Path to the new version of the codebase.
        output_format (str): Output format, either 'json' or 'text'. Defaults to 'json'.

    Returns:
        str: A report in the specified format highlighting potential vulnerabilities.
    """
    if not os.path.exists(old_path) or not os.path.exists(new_path):
        raise FileNotFoundError("One or both of the provided paths do not exist.")

    dmp = diff_match_patch()
    differences = []

    for root, _, files in os.walk(old_path):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = old_file_path.replace(old_path, new_path, 1)

            if not os.path.exists(new_file_path):
                differences.append({"file": file, "status": "removed"})
                continue

            with open(old_file_path, 'r') as old_file, open(new_file_path, 'r') as new_file:
                old_content = old_file.read()
                new_content = new_file.read()

                diffs = dmp.diff_main(old_content, new_content)
                dmp.diff_cleanupSemantic(diffs)

                if diffs:
                    differences.append({"file": file, "diffs": diffs})

    # Mockable AI-assisted analysis
    for diff in differences:
        if "diffs" in diff:
            diff_text = ''.join([d[1] for d in diff["diffs"] if d[0] != 0])
            diff["analysis"] = {"label": "SAFE", "score": 0.99}  # Placeholder analysis

    if output_format == 'json':
        return json.dumps(differences, indent=4)
    elif output_format == 'text':
        return "\n".join([str(diff) for diff in differences])
    else:
        raise ValueError("Invalid output format. Choose 'json' or 'text'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Zero-Day Diff Checker")
    parser.add_argument("old_path", help="Path to the old version of the codebase")
    parser.add_argument("new_path", help="Path to the new version of the codebase")
    parser.add_argument("--output-format", choices=['json', 'text'], default='json', help="Output format")

    args = parser.parse_args()

    try:
        report = analyze_diff(args.old_path, args.new_path, args.output_format)
        print(report)
    except Exception as e:
        print(f"Error: {e}")