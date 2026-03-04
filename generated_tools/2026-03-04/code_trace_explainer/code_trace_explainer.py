import argparse
import json
import openai

def analyze_trace(trace_data):
    """
    Analyze the trace data and generate a detailed explanation.

    Args:
        trace_data (dict): The JSON-formatted trace data.

    Returns:
        str: A detailed explanation of the execution flow.
    """
    explanation = []

    for entry in trace_data.get("trace", []):
        function_name = entry.get("function", "<unknown>")
        line_number = entry.get("line", "<unknown>")
        variables = entry.get("variables", {})

        explanation.append(f"Function: {function_name}, Line: {line_number}")
        explanation.append("Variables:")
        for var_name, var_value in variables.items():
            explanation.append(f"  {var_name}: {var_value}")
        explanation.append("")

    return "\n".join(explanation).strip()

def generate_ai_insights(trace_analysis):
    """
    Use OpenAI to generate insights on the trace analysis.

    Args:
        trace_analysis (str): The trace analysis explanation.

    Returns:
        str: AI-generated insights.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                "Analyze the following code execution trace and provide insights on the flow, "
                "variable states, and potential logic issues:\n\n" + trace_analysis
            ),
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating AI insights: {e}"

def main():
    parser = argparse.ArgumentParser(description="Code Trace Explainer")
    parser.add_argument("--tracefile", required=True, help="Path to the JSON-formatted trace file")
    args = parser.parse_args()

    try:
        with open(args.tracefile, "r") as f:
            trace_data = json.load(f)
    except FileNotFoundError:
        print("Error: Trace file not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in trace file.")
        return

    trace_analysis = analyze_trace(trace_data)
    print("Trace Analysis:")
    print(trace_analysis)

    ai_insights = generate_ai_insights(trace_analysis)
    print("\nAI Insights:")
    print(ai_insights)

if __name__ == "__main__":
    main()