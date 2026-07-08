import argparse
import regex as re
import spacy
import sys

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except Exception as e:
        raise RuntimeError("Failed to load spaCy model. Ensure 'en_core_web_sm' is installed.")

def detect_pii(text, nlp):
    sensitive_patterns = {
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "phone": r"\b\d{10}\b|\b\d{3}-\d{3}-\d{4}\b",
        "credit_card": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b|\b\d{16}\b"
    }

    flagged_items = []

    for label, pattern in sensitive_patterns.items():
        matches = re.findall(pattern, text)
        flagged_items.extend([(label, match.strip().rstrip('.')) for match in matches])

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            flagged_items.append((ent.label_, ent.text.strip()))

    return flagged_items

def scan_file(file_path, pii_check):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    nlp = load_spacy_model()
    if pii_check:
        return detect_pii(content, nlp)
    return []

def main():
    parser = argparse.ArgumentParser(description="AI Privacy Audit Tool")
    parser.add_argument("--logfile", type=str, help="Path to the log file to scan.")
    parser.add_argument("--pii-check", action="store_true", help="Enable PII detection.")

    args = parser.parse_args()

    if not args.logfile:
        print("Error: --logfile argument is required.", file=sys.stderr)
        sys.exit(1)

    try:
        results = scan_file(args.logfile, args.pii_check)
        if results:
            print("Sensitive data found:")
            for label, item in results:
                print(f"- {label}: {item}")
        else:
            print("No sensitive data found.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
