import openai
import click
import sh
import os
from typing import Optional

def validate_script(script: str, shell: str) -> bool:
    """Validate the generated script for dangerous operations."""
    dangerous_commands = ['rm -rf', 'dd if=', ':(){:|:&};:']
    for command in dangerous_commands:
        if command in script:
            return False
    return True

def generate_script(instruction: str, shell: str) -> str:
    """Generate a shell script using OpenAI's GPT API."""
    try:
        response = openai.Completion.create(
            engine="gpt-5.4",
            prompt=f"Generate a secure {shell} script for the following instruction: {instruction}",
            max_tokens=200
        )
        script = response.choices[0].text.strip()
        return script
    except Exception as e:
        raise RuntimeError(f"Failed to generate script: {e}")

def execute_script(script: str, shell: str) -> None:
    """Execute the generated script after user confirmation."""
    print("Generated script:")
    print(script)
    confirm = input("Do you want to execute this script? (yes/no): ").strip().lower()
    if confirm == 'yes':
        try:
            if shell == 'bash':
                sh.bash('-c', script)
            elif shell == 'powershell':
                sh.powershell('-Command', script)
            else:
                raise ValueError("Unsupported shell type")
        except Exception as e:
            raise RuntimeError(f"Error executing script: {e}")
    else:
        print("Execution cancelled.")

@click.command()
@click.option('--instruction', required=True, help='Plain English instruction for the script.')
@click.option('--shell', default='bash', type=click.Choice(['bash', 'powershell']), help='Shell type (bash or PowerShell).')
@click.option('--execute', is_flag=True, help='Execute the generated script after validation.')
def main(instruction: str, shell: str, execute: bool):
    """Main CLI entry point."""
    try:
        script = generate_script(instruction, shell)
        if not validate_script(script, shell):
            raise ValueError("Generated script contains potentially dangerous commands.")

        if execute:
            execute_script(script, shell)
        else:
            print("Generated script:")
            print(script)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()