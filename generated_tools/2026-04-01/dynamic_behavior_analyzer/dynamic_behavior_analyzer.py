import argparse
import json
import os
import subprocess
import tracemalloc
from tempfile import TemporaryDirectory

def analyze_script(script_path, output_path, runtime_args):
    """
    Executes the given script in a controlled environment and monitors its behavior.

    Args:
        script_path (str): Path to the script to analyze.
        output_path (str): Path to save the behavior report.
        runtime_args (list): List of arguments to pass to the script.

    Returns:
        dict: A dictionary containing the behavior analysis report.
    """
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file '{script_path}' not found.")

    report = {
        "script": script_path,
        "runtime_args": runtime_args,
        "memory_usage": [],
        "suspicious_patterns": []
    }

    tracemalloc.start()

    with TemporaryDirectory() as sandbox_dir:
        try:
            # Copy the script into the sandbox
            sandbox_script_path = os.path.join(sandbox_dir, os.path.basename(script_path))
            with open(script_path, "r") as src, open(sandbox_script_path, "w") as dst:
                dst.write(src.read())

            # Run the script in a subprocess
            process = subprocess.Popen(
                ["python", sandbox_script_path] + runtime_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            # Capture memory usage
            snapshot = tracemalloc.take_snapshot()
            for stat in snapshot.statistics("lineno")[:10]:
                report["memory_usage"].append({
                    "trace": str(stat.traceback),
                    "size": stat.size
                })

            # Analyze output for suspicious patterns
            suspicious_keywords = ["undercover", "bypass", "hidden"]
            for keyword in suspicious_keywords:
                if keyword in stdout.lower() or keyword in stderr.lower():
                    report["suspicious_patterns"].append(keyword)

            # Add stdout and stderr to the report
            report["stdout"] = stdout
            report["stderr"] = stderr

        except Exception as e:
            report["error"] = str(e)

    # Save the report to a JSON file
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    return report

def main():
    parser = argparse.ArgumentParser(description="Dynamic Behavior Analyzer")
    parser.add_argument("--script", required=True, help="Path to the script to analyze.")
    parser.add_argument("--output", required=True, help="Path to save the behavior report.")
    parser.add_argument("--args", nargs=argparse.REMAINDER, default=[], help="Optional arguments to pass to the script.")

    args = parser.parse_args()

    try:
        report = analyze_script(args.script, args.output, args.args)
        print(f"Behavior analysis completed. Report saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()