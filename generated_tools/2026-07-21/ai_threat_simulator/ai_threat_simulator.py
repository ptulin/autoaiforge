import argparse
import requests
from faker import Faker

def simulate_spoof_attack(target, frequency):
    """Simulate a spoofed API call attack."""
    fake = Faker()
    logs = []
    for _ in range(frequency):
        spoofed_ip = fake.ipv4()
        headers = {"X-Forwarded-For": spoofed_ip}
        try:
            response = requests.get(target, headers=headers, timeout=5)
            logs.append({
                "spoofed_ip": spoofed_ip,
                "status_code": response.status_code,
                "response": response.text
            })
        except requests.RequestException as e:
            logs.append({
                "spoofed_ip": spoofed_ip,
                "error": str(e)
            })
    return logs

def simulate_brute_force_attack(target, frequency):
    """Simulate a brute force attack."""
    fake = Faker()
    logs = []
    for _ in range(frequency):
        username = fake.user_name()
        password = fake.password()
        payload = {"username": username, "password": password}
        try:
            response = requests.post(target, data=payload, timeout=5)
            logs.append({
                "username": username,
                "password": password,
                "status_code": response.status_code,
                "response": response.text
            })
        except requests.RequestException as e:
            logs.append({
                "username": username,
                "password": password,
                "error": str(e)
            })
    return logs

def simulate_data_exfiltration(target, payload_size):
    """Simulate a data exfiltration attack."""
    fake = Faker()
    logs = []
    payload = fake.text(max_nb_chars=payload_size)
    payload = payload.ljust(payload_size)[:payload_size]  # Ensure payload size matches exactly
    try:
        response = requests.post(target, data={"data": payload}, timeout=5)
        logs.append({
            "payload_size": len(payload),
            "status_code": response.status_code,
            "response": response.text
        })
    except requests.RequestException as e:
        logs.append({
            "payload_size": len(payload),
            "error": str(e)
        })
    return logs

def main():
    parser = argparse.ArgumentParser(description="AI Threat Simulator")
    parser.add_argument("--attack", required=True, choices=["spoof", "brute", "exfiltration"], help="Type of attack to simulate")
    parser.add_argument("--target", required=True, help="Target endpoint URL")
    parser.add_argument("--frequency", type=int, default=1, help="Number of attack attempts (default: 1)")
    parser.add_argument("--payload_size", type=int, default=100, help="Payload size for data exfiltration (default: 100 characters)")

    args = parser.parse_args()

    if args.attack == "spoof":
        logs = simulate_spoof_attack(args.target, args.frequency)
    elif args.attack == "brute":
        logs = simulate_brute_force_attack(args.target, args.frequency)
    elif args.attack == "exfiltration":
        logs = simulate_data_exfiltration(args.target, args.payload_size)
    else:
        raise ValueError("Unsupported attack type")

    for log in logs:
        print(log)

if __name__ == "__main__":
    main()
