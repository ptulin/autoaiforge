import os
import json
import ast
import random
import argparse
from black import format_str, FileMode

def inject_syntax_error(code):
    """Injects a syntax error into the provided code."""
    return code + "\nprint(\"Unclosed string\")"

def inject_logic_error(code):
    """Injects a logic error by modifying a comparison."""
    tree = ast.parse(code)
    class LogicErrorTransformer(ast.NodeTransformer):
        def visit_Compare(self, node):
            if isinstance(node.ops[0], ast.Eq):
                node.ops[0] = ast.NotEq()
            return node
    tree = LogicErrorTransformer().visit(tree)
    return ast.unparse(tree)

def inject_runtime_error(code):
    """Injects a runtime error by dividing by zero."""
    return code + "\nresult = 1 / 0"

BUG_INJECTORS = {
    "syntax": inject_syntax_error,
    "logic": inject_logic_error,
    "runtime": inject_runtime_error
}

def inject_bug(file_path, bug_type):
    """Injects a specified type of bug into a Python file."""
    with open(file_path, "r") as f:
        code = f.read()

    if bug_type not in BUG_INJECTORS:
        raise ValueError(f"Unsupported bug type: {bug_type}")

    buggy_code = BUG_INJECTORS[bug_type](code)
    try:
        formatted_code = format_str(buggy_code, mode=FileMode())
    except Exception as e:
        raise ValueError(f"Failed to format code: {e}")

    return formatted_code

def save_buggy_code(file_path, buggy_code):
    """Saves buggy code to the specified file."""
    with open(file_path, "w") as f:
        f.write(buggy_code)

def generate_test_case(file_path):
    """Generates a simple test case for the buggy file."""
    test_code = f"""import pytest\n\ndef test_placeholder():\n    assert True  # Replace with actual test logic\n"""
    test_file_path = file_path.replace(".py", "_test.py")
    with open(test_file_path, "w") as f:
        f.write(test_code)

def process_codebase(code_dir, config_path):
    """Processes the codebase to inject bugs and generate test cases."""
    if not os.path.exists(code_dir):
        raise FileNotFoundError(f"Code directory not found: {code_dir}")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    for file_config in config.get("files", []):
        file_path = os.path.join(code_dir, file_config["file"])
        bug_type = file_config["bug_type"]

        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            continue

        try:
            buggy_code = inject_bug(file_path, bug_type)
            save_buggy_code(file_path, buggy_code)
            generate_test_case(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Debugging Task Generator")
    parser.add_argument("--code_dir", required=True, help="Path to the directory containing Python source code files.")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file specifying bug types and locations.")

    args = parser.parse_args()

    try:
        process_codebase(args.code_dir, args.config)
    except Exception as e:
        print(f"Error: {e}")