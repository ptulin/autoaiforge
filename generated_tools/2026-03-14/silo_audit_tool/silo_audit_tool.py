import argparse
import json
import logging
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def setup_logging(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def perform_integrity_check(file_path):
    try:
        if not os.path.isfile(file_path):
            logging.error("File not found: %s", file_path)
            return False

        with open(file_path, 'rb') as f:
            data = f.read()

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data)
        checksum = digest.finalize()

        logging.info("Integrity check passed for file: %s", file_path)
        return checksum.hex()

    except Exception as e:
        logging.error("Error during integrity check: %s", str(e))
        return False

def log_access_event(file_path, success):
    event = {
        "file": file_path,
        "access_success": success,
        "event": "access_attempt"
    }
    logging.info("Access event: %s", json.dumps(event))
    return event

def generate_report(events, report_format):
    if report_format == 'json':
        return json.dumps(events, indent=4)
    else:
        logging.error("Unsupported report format: %s", report_format)
        return None

def main():
    parser = argparse.ArgumentParser(description="Silo Audit Tool: Audit and monitor encrypted data silos.")
    parser.add_argument('--silo', required=True, help="Path to the encrypted data silo.")
    parser.add_argument('--loglevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level.")
    parser.add_argument('--report', default='json', choices=['json'], help="Format of the audit report.")

    args = parser.parse_args()

    setup_logging(getattr(logging, args.loglevel.upper(), logging.INFO))

    logging.info("Starting Silo Audit Tool")

    events = []

    # Log access attempt
    access_event = log_access_event(args.silo, success=True)
    events.append(access_event)

    # Perform integrity check
    integrity_result = perform_integrity_check(args.silo)
    if integrity_result:
        events.append({"file": args.silo, "integrity_check": "passed", "checksum": integrity_result})
    else:
        events.append({"file": args.silo, "integrity_check": "failed"})

    # Generate report
    report = generate_report(events, args.report)
    if report:
        print(report)

if __name__ == "__main__":
    main()
