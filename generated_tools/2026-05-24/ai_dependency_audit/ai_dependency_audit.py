import os
import json
import pkg_resources
import openai

def audit_dependencies(file_path):
    """
    Analyze project dependencies for security vulnerabilities and suggest safer alternatives.

    Args:
        file_path (str): Path to the dependency file (e.g., requirements.txt or package.json).

    Returns:
        list: A list of dictionaries containing information about flagged vulnerabilities and suggestions.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as f:
        content = f.read()

    dependencies = parse_dependencies(file_path, content)

    if not dependencies:
        return []

    vulnerabilities = []

    for dep in dependencies:
        try:
            package_name, current_version = dep['name'], dep['version']
            latest_version, risk_level, safer_alternatives = analyze_dependency(package_name, current_version)
            if risk_level != "safe":
                vulnerabilities.append({
                    "package": package_name,
                    "current_version": current_version,
                    "latest_version": latest_version,
                    "risk_level": risk_level,
                    "safer_alternatives": safer_alternatives
                })
        except Exception as e:
            vulnerabilities.append({
                "package": dep['name'],
                "error": str(e)
            })

    return vulnerabilities

def parse_dependencies(file_path, content):
    """
    Parse the dependency file and extract package names and versions.

    Args:
        file_path (str): Path to the dependency file.
        content (str): Content of the dependency file.

    Returns:
        list: A list of dictionaries with package names and versions.
    """
    dependencies = []

    if file_path.endswith('requirements.txt'):
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    package = pkg_resources.Requirement.parse(line)
                    if package.specs:
                        dependencies.append({"name": package.project_name, "version": package.specs[0][1]})
                    else:
                        dependencies.append({"name": package.project_name, "version": "latest"})
                except Exception:
                    continue

    elif file_path.endswith('package.json'):
        try:
            package_json = json.loads(content)
            for package_name, version in package_json.get('dependencies', {}).items():
                dependencies.append({"name": package_name, "version": version})
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in package.json")

    else:
        raise ValueError("Unsupported file format. Only requirements.txt and package.json are supported.")

    return dependencies

def analyze_dependency(package_name, current_version):
    """
    Analyze a single dependency for vulnerabilities using AI.

    Args:
        package_name (str): Name of the package.
        current_version (str): Current version of the package.

    Returns:
        tuple: (latest_version, risk_level, safer_alternatives)
    """
    # Simulate an API call to OpenAI for vulnerability analysis
    try:
        # Replace this with your OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

        prompt = (
            f"Analyze the following Python package for vulnerabilities:\n"
            f"Package: {package_name}\n"
            f"Version: {current_version}\n"
            f"Provide the latest version, risk level (safe, moderate, high), and safer alternatives if any."
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        analysis = json.loads(response.choices[0].text.strip())

        return (
            analysis.get("latest_version", "unknown"),
            analysis.get("risk_level", "unknown"),
            analysis.get("safer_alternatives", [])
        )
    except Exception as e:
        raise RuntimeError(f"Failed to analyze dependency {package_name}: {str(e)}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Audit project dependencies for vulnerabilities.")
    parser.add_argument("file_path", type=str, help="Path to the dependency file (e.g., requirements.txt or package.json).")
    args = parser.parse_args()

    try:
        results = audit_dependencies(args.file_path)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")