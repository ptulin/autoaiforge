import os
import argparse
import subprocess
import shutil
import openai
from datetime import datetime

def fetch_patch_suggestions(project_path):
    """Fetch patch suggestions using OpenAI API."""
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Analyze the codebase at {project_path} and suggest patches for vulnerabilities.",
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error fetching patch suggestions: {str(e)}"

def apply_patch(patch_content, project_path):
    """Apply the patch to the codebase."""
    try:
        patch_file = os.path.join(project_path, "patch.diff")
        with open(patch_file, "w") as f:
            f.write(patch_content)

        result = subprocess.run(
            ["patch", "-p1"],
            input=patch_content,
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "Patch applied successfully."
        else:
            return f"Failed to apply patch: {result.stderr}"
    except Exception as e:
        return f"Error applying patch: {str(e)}"

def sandbox_test_patch(project_path):
    """Test the patch in a sandbox environment."""
    try:
        sandbox_path = os.path.join(project_path, "sandbox")
        shutil.copytree(project_path, sandbox_path)

        # Simulate testing (this can be extended)
        test_result = subprocess.run(
            ["python", "-m", "unittest"],
            cwd=sandbox_path,
            capture_output=True,
            text=True
        )

        shutil.rmtree(sandbox_path)

        if test_result.returncode == 0:
            return "Sandbox testing passed."
        else:
            return f"Sandbox testing failed: {test_result.stderr}"
    except Exception as e:
        return f"Error during sandbox testing: {str(e)}"

def rollback_patch(project_path):
    """Rollback the last applied patch."""
    try:
        result = subprocess.run(
            ["patch", "-R", "-p1"],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "Patch rolled back successfully."
        else:
            return f"Failed to rollback patch: {result.stderr}"
    except Exception as e:
        return f"Error rolling back patch: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Auto Patch Applier")
    parser.add_argument("--path", required=True, help="Path to the project directory")
    parser.add_argument("--test_sandbox", action="store_true", help="Enable sandbox testing")
    parser.add_argument("--rollback", action="store_true", help="Rollback the last applied patch")

    args = parser.parse_args()

    project_path = args.path

    if not os.path.exists(project_path):
        print("Error: The specified project path does not exist.")
        return

    log_file = os.path.join(project_path, "patch_log.txt")

    if args.rollback:
        result = rollback_patch(project_path)
        with open(log_file, "a") as log:
            log.write(f"[{datetime.now()}] Rollback: {result}\n")
        print(result)
        return

    patch_suggestions = fetch_patch_suggestions(project_path)

    if "Error" in patch_suggestions:
        print(patch_suggestions)
        return

    if args.test_sandbox:
        test_result = sandbox_test_patch(project_path)
        if "failed" in test_result.lower():
            print(test_result)
            return

    apply_result = apply_patch(patch_suggestions, project_path)

    with open(log_file, "a") as log:
        log.write(f"[{datetime.now()}] Patch applied: {apply_result}\n")

    print(apply_result)

if __name__ == "__main__":
    main()
