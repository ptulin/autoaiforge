import os
import argparse
import openai
import pylint.lint

class AICodeLinter:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def lint_code(self, file_path):
        """Run pylint on the given file and return the linting report."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File or directory not found: {file_path}")

        pylint_output = []
        try:
            pylint_opts = [file_path]
            pylint_runner = pylint.lint.Run(pylint_opts, do_exit=False)
            pylint_output = [
                {
                    "type": msg.category,
                    "module": msg.module,
                    "line": msg.line,
                    "message": msg.msg
                }
                for msg in pylint_runner.linter.reporter.messages
            ]
        except Exception as e:
            raise RuntimeError(f"Error running pylint: {e}")

        return pylint_output

    def analyze_with_ai(self, code):
        """Use OpenAI to analyze the code and provide recommendations."""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Analyze the following Python code for issues and suggest improvements:\n\n{code}",
                max_tokens=500
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            raise RuntimeError(f"Error analyzing code with OpenAI: {e}")

    def process_path(self, path, fix=False):
        """Process a file or directory for linting and AI analysis."""
        if os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.py')]
        elif os.path.isfile(path):
            files = [path]
        else:
            raise FileNotFoundError(f"Invalid path: {path}")

        results = {}
        for file in files:
            with open(file, 'r') as f:
                code = f.read()

            pylint_report = self.lint_code(file)
            ai_analysis = self.analyze_with_ai(code)

            results[file] = {
                'pylint_report': pylint_report,
                'ai_analysis': ai_analysis
            }

            if fix:
                # Placeholder for auto-fix logic
                pass

        return results

def main():
    parser = argparse.ArgumentParser(description="AI Code Linter: Analyze Python code for issues and improvements.")
    parser.add_argument('--path', required=True, help="Path to the Python file or directory to lint.")
    parser.add_argument('--fix', action='store_true', help="Automatically fix issues where possible.")
    parser.add_argument('--api-key', required=True, help="OpenAI API key for AI analysis.")

    args = parser.parse_args()

    linter = AICodeLinter(api_key=args.api_key)

    try:
        results = linter.process_path(args.path, fix=args.fix)
        for file, report in results.items():
            print(f"\nFile: {file}")
            print("Pylint Report:")
            for issue in report['pylint_report']:
                print(f"{issue['type']} - {issue['module']}:{issue['line']} - {issue['message']}")
            print("\nAI Analysis:")
            print(report['ai_analysis'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
