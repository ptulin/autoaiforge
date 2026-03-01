import argparse
import pandas as pd
import yaml
import os
import json

def load_rules(rules_path):
    """Load ethical rules from a YAML file."""
    try:
        with open(rules_path, 'r') as file:
            rules = yaml.safe_load(file)
        return rules
    except FileNotFoundError:
        raise FileNotFoundError(f"Rules file not found: {rules_path}")
    except yaml.YAMLError:
        raise ValueError(f"Invalid YAML format in rules file: {rules_path}")

def load_log(log_path):
    """Load decision logs from a CSV or JSON file."""
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found: {log_path}")

    try:
        if log_path.endswith('.csv'):
            return pd.read_csv(log_path)
        elif log_path.endswith('.json'):
            return pd.read_json(log_path)
        else:
            raise ValueError("Unsupported log file format. Use CSV or JSON.")
    except Exception as e:
        raise ValueError(f"Error loading log file: {e}")

def audit_decisions(log_df, rules):
    """Audit decisions based on ethical rules."""
    flagged_decisions = []

    for _, row in log_df.iterrows():
        row_dict = row.to_dict()
        for rule in rules.get('rules', []):
            condition = rule.get('condition')
            explanation = rule.get('explanation')

            if condition and explanation:
                try:
                    if eval(condition, {"__builtins__": None}, {"row": row_dict}):
                        flagged_decisions.append({
                            'decision_id': row_dict.get('decision_id', 'N/A'),
                            'condition': condition,
                            'explanation': explanation
                        })
                except Exception as e:
                    print(f"Error evaluating condition '{condition}' on row {row_dict}: {e}")

    return flagged_decisions

def save_results(flagged_decisions, output_path):
    """Save flagged decisions to a CSV or JSON file."""
    if output_path.endswith('.csv'):
        pd.DataFrame(flagged_decisions).to_csv(output_path, index=False)
    elif output_path.endswith('.json'):
        with open(output_path, 'w') as file:
            json.dump(flagged_decisions, file, indent=4)
    else:
        raise ValueError("Unsupported output file format. Use CSV or JSON.")

def main():
    parser = argparse.ArgumentParser(description="AI Decision Audit Tool")
    parser.add_argument('--log', required=True, help="Path to the AI decision log file (CSV or JSON).")
    parser.add_argument('--rules', required=True, help="Path to the YAML file containing ethical rules.")
    parser.add_argument('--output', help="Optional path to save flagged decisions (CSV or JSON).")

    args = parser.parse_args()

    try:
        rules = load_rules(args.rules)
        log_df = load_log(args.log)
        flagged_decisions = audit_decisions(log_df, rules)

        print(f"Found {len(flagged_decisions)} flagged decisions.")
        for decision in flagged_decisions:
            print(f"Decision ID: {decision['decision_id']}, Explanation: {decision['explanation']}")

        if args.output:
            save_results(flagged_decisions, args.output)
            print(f"Flagged decisions saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()