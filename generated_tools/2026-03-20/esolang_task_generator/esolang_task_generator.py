import random
from pyparsing import Word, alphas, nums, Optional, ParseException

def generate_brainfuck_task(complexity):
    """
    Generate a random Brainfuck program based on the given complexity.

    Args:
        complexity (int): Determines the length and complexity of the program.

    Returns:
        str: A randomly generated Brainfuck program.
    """
    commands = ['>', '<', '+', '-', '.', ',', '[', ']']
    program = ''.join(random.choices(commands, k=complexity))
    return program

def validate_brainfuck_syntax(program):
    """
    Validate the syntax of a Brainfuck program.

    Args:
        program (str): The Brainfuck program to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    stack = []
    for char in program:
        if char == '[':
            stack.append('[')
        elif char == ']':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def generate_task(language='brainfuck', complexity=5):
    """
    Generate a task in the specified esoteric language.

    Args:
        language (str): The target esoteric language (default: 'brainfuck').
        complexity (int): The complexity level of the task (default: 5).

    Returns:
        str: The generated task as a string.

    Raises:
        ValueError: If the language is unsupported or complexity is invalid.
    """
    if complexity <= 0:
        raise ValueError("Complexity must be a positive integer.")

    if language == 'brainfuck':
        task = generate_brainfuck_task(complexity)
        if not validate_brainfuck_syntax(task):
            raise ValueError("Generated Brainfuck program has invalid syntax.")
        return task
    else:
        raise ValueError(f"Unsupported language: {language}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Esoteric Task Generator")
    parser.add_argument("--language", type=str, default="brainfuck", help="Target esoteric language (default: brainfuck)")
    parser.add_argument("--complexity", type=int, default=5, help="Complexity level of the task (default: 5)")

    args = parser.parse_args()

    try:
        task = generate_task(language=args.language, complexity=args.complexity)
        print("Generated Task:")
        print(task)
    except ValueError as e:
        print(f"Error: {e}")