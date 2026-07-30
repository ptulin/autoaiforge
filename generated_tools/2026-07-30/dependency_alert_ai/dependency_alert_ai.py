import argparse
import json
import os
from packaging.version import parse as parse_version
import requests
import openai

def fetch_vulnerability_data(package_name, version):
    """Fetch vulnerability data for a specific package and version."""
    try:
        response = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={package_name}")
        response.raise_for_status()
        vulnerabilities = []
        data = response.json()
        for item in data.get("result", {}).get("CVE_Items", []):
            for node in item.get("configurations", {}).get("nodes", []):
                for cpe_match in node.get("cpe_match", []):
                    if package_name in cpe_match.get("cpe23Uri", "") and version in cpe_match.get("cpe23Uri", ""):
                        vulnerabilities.append(item["cve"])
        return vulnerabilities
    except requests.RequestException as e:
        return {"error": str(e)}

def analyze_dependencies(requirements_file):
    """Analyze dependencies for vulnerabilities."""
    if not os.path.exists(requirements_file):
        return {"error": f"File {requirements_file} does not exist."}

    results = {}
    with open(requirements_file, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "==" in line:
                package_name, version = line.split("==")
                version = version.strip()
            else:
                package_name = line
                version = None

            if version:
                vulnerabilities = fetch_vulnerability_data(package_name, version)
                if vulnerabilities:
                    results[package_name] = {
                        "version": version,
                        "vulnerabilities": vulnerabilities,
                    }
    return results

def main():
    parser = argparse.ArgumentParser(description="Dependency Alert AI: Analyze dependencies for vulnerabilities.")
    parser.add_argument("--requirements", required=True, help="Path to the requirements.txt file")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="Output format")
    args = parser.parse_args()

    results = analyze_dependencies(args.requirements)

    if "error" in results:
        print(f"Error: {results['error']}")
        return

    if args.output == "json":
        print(json.dumps(results, indent=4))
    else:
        for package, data in results.items():
            print(f"Package: {package}")
            print(f"Version: {data['version']}")
            print("Vulnerabilities:")
            for vuln in data["vulnerabilities"]:
                print(f"  - {vuln['CVE_data_meta']['ID']}: {vuln['description']['description_data'][0]['value']}")
            print()

if __name__ == "__main__":
    main()