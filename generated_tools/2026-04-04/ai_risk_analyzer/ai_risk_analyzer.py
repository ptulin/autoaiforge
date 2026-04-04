import argparse
import subprocess
import psutil
import json
import os
import tempfile
from typing import Dict, List

def run_script_in_sandbox(script_path: str) -> Dict:
    """
    Runs the given script in a sandboxed environment and monitors its behavior.

    Args:
        script_path (str): Path to the script to be analyzed.

    Returns:
        Dict: A dictionary containing monitored process information.
    """
    try:
        with tempfile.TemporaryDirectory() as sandbox_dir:
            process = subprocess.Popen(
                ["python", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=sandbox_dir
            )
            try:
                process_info = psutil.Process(process.pid)
                stdout, stderr = process.communicate(timeout=10)
                return {
                    "pid": process.pid,
                    "stdout": stdout.decode("utf-8"),
                    "stderr": stderr.decode("utf-8"),
                    "open_files": [f.path for f in process_info.open_files()],
                    "connections": [conn.raddr for conn in process_info.connections()]
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {"error": "Script execution timed out"}
    except Exception as e:
        return {"error": str(e)}

def analyze_risks(monitored_data: Dict, risk_rules: Dict) -> List[Dict]:
    """
    Analyzes the monitored data for potential risks based on the provided rules.

    Args:
        monitored_data (Dict): Data collected from the sandboxed execution.
        risk_rules (Dict): Risk rules defined in the JSON file.

    Returns:
        List[Dict]: A list of flagged risks.
    """
    flagged_risks = []

    for rule in risk_rules.get("rules", []):
        if rule.get("type") == "file_access" and monitored_data.get("open_files"):
            for file in monitored_data["open_files"]:
                if rule.get("match") in file:
                    flagged_risks.append({
                        "type": "file_access",
                        "rule": rule,
                        "detail": file
                    })

        if rule.get("type") == "network_access" and monitored_data.get("connections"):
            for conn in monitored_data["connections"]:
                if rule.get("match") in conn:
                    flagged_risks.append({
                        "type": "network_access",
                        "rule": rule,
                        "detail": conn
                    })

    return flagged_risks

def main():
    parser = argparse.ArgumentParser(description="AI Risk Analyzer")
    parser.add_argument("--script", required=True, help="Path to the Python script to analyze")
    parser.add_argument("--rules", required=True, help="Path to the JSON file containing risk rules")
    parser.add_argument("--output", required=True, help="Path to save the JSON report")

    args = parser.parse_args()

    if not os.path.exists(args.script):
        print(f"Error: Script file '{args.script}' not found.")
        return

    if not os.path.exists(args.rules):
        print(f"Error: Rules file '{args.rules}' not found.")
        return

    try:
        with open(args.rules, "r") as rules_file:
            risk_rules = json.load(rules_file)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from '{args.rules}'.")
        return

    monitored_data = run_script_in_sandbox(args.script)

    if "error" in monitored_data:
        print(f"Error during script execution: {monitored_data['error']}")
        return

    flagged_risks = analyze_risks(monitored_data, risk_rules)

    report = {
        "script": args.script,
        "monitored_data": monitored_data,
        "flagged_risks": flagged_risks
    }

    try:
        with open(args.output, "w") as output_file:
            json.dump(report, output_file, indent=4)
        print(f"Risk analysis report saved to '{args.output}'.")
    except Exception as e:
        print(f"Error: Failed to save report. {str(e)}")

if __name__ == "__main__":
    main()