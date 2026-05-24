import argparse
import os
import difflib
import openai

def analyze_vulnerability(file_path):
    """
    Analyze the source code file for vulnerabilities and generate a patch.

    Args:
        file_path (str): Path to the source code file.

    Returns:
        tuple: (vulnerable_code, suggested_patch)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        source_code = file.read()

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following code for vulnerabilities and suggest a patch:\n\n{source_code}\n\nVulnerable code and patch:",
            max_tokens=500
        )
        result = response['choices'][0]['text'].strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate patch: {e}")

    # Split the response into vulnerable code and patch
    if "Suggested Patch:" in result:
        vulnerable_code, suggested_patch = result.split("Suggested Patch:", 1)
        return vulnerable_code.strip(), suggested_patch.strip()
    else:
        raise ValueError("Unexpected response format from AI.")

def generate_patch_file(vulnerable_code, suggested_patch, output_path):
    """
    Generate a .patch file with the suggested fixes.

    Args:
        vulnerable_code (str): The vulnerable code snippet.
        suggested_patch (str): The AI-suggested patch.
        output_path (str): Path to save the .patch file.
    """
    patch_content = difflib.unified_diff(
        vulnerable_code.splitlines(),
        suggested_patch.splitlines(),
        lineterm='',
        fromfile='vulnerable_code',
        tofile='suggested_patch'
    )

    with open(output_path, 'w') as patch_file:
        patch_file.write('\n'.join(patch_content))

def main():
    parser = argparse.ArgumentParser(description="AI-Driven Patch Generator")
    parser.add_argument('--file', required=True, help="Path to the source code file containing a known vulnerability.")
    parser.add_argument('--output', required=True, help="Path to save the AI-generated patch file.")
    args = parser.parse_args()

    try:
        vulnerable_code, suggested_patch = analyze_vulnerability(args.file)
        generate_patch_file(vulnerable_code, suggested_patch, args.output)
        print("Patch file generated successfully:", args.output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
