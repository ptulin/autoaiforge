import argparse
import openai
import os

def enhance_script(input_path, tone):
    """
    Enhances the script by analyzing character dialogue, fixing grammar,
    and adjusting tone based on user preferences.

    Args:
        input_path (str): Path to the input script file.
        tone (str): Desired tone/style for the script.

    Returns:
        str: Enhanced script text.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file '{input_path}' does not exist.")

    with open(input_path, 'r') as file:
        script_content = file.read()

    if not script_content.strip():
        raise ValueError("The input file is empty.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI script enhancer. Improve the script by enhancing dialogue, fixing grammar, and adjusting tone."},
                {"role": "user", "content": f"Tone: {tone}\nScript:\n{script_content}"}
            ]
        )
        enhanced_script = response['choices'][0]['message']['content']
        return enhanced_script

    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to process the script: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="AI Script Enhancer: Improve your scripts with AI suggestions.")
    parser.add_argument('--input', required=True, help="Path to the input script file.")
    parser.add_argument('--tone', required=True, help="Desired tone/style for the script (e.g., formal, casual, dramatic).")
    parser.add_argument('--output', help="Path to save the enhanced script. If not provided, prints to stdout.")

    args = parser.parse_args()

    try:
        enhanced_script = enhance_script(args.input, args.tone)

        if args.output:
            with open(args.output, 'w') as file:
                file.write(enhanced_script)
            print(f"Enhanced script saved to {args.output}")
        else:
            print("Enhanced Script:\n")
            print(enhanced_script)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()